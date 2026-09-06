import os
import shutil
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
from app.database import SessionLocal
from app.models import Provider, Scenario, TestConfiguration, Campaign, TestRun, Target, Strategy
from app.adapters import AdapterRequest, get_adapter

ARTIFACT_ROOT = Path(os.getenv("ARTIFACT_ROOT", "/tmp/redteam-artifacts"))

def _execute_one(campaign_id, target_endpoint, provider_name, scenario, attempt, strategy_config):
    db = SessionLocal()
    tr = None
    try:
        tr = TestRun(campaign_id=campaign_id, provider=provider_name, scenario=scenario.key, attempt=attempt, status="RUNNING")
        db.add(tr); db.commit(); db.refresh(tr)
        adapter = get_adapter(provider_name)
        artifact_dir = ARTIFACT_ROOT / str(campaign_id) / str(tr.id)
        request = AdapterRequest(target_endpoint, scenario.key, scenario.category, scenario.prompt_template, attempt,
                                 {"severity": scenario.severity, "strategy": strategy_config,
                                  "timeout_seconds": strategy_config.get("timeout_seconds", 60), "artifact_dir": str(artifact_dir)})
        retries = max(0, min(3, int(strategy_config.get("retries", 1))))
        result = None
        for retry in range(retries + 1):
            result = adapter.normalize(adapter.execute(request))
            if result.status not in {"FAILED", "TIMEOUT"} or retry == retries:
                break
        tr.status, tr.success, tr.severity = result.status, result.success, result.severity
        tr.request, tr.response, tr.evidence = result.request, result.response, {**result.evidence, "retries": retry}
        db.commit(); return tr.status
    except Exception as exc:
        if tr is not None:
            tr.status, tr.success, tr.severity = "FAILED", False, "INFO"
            tr.request, tr.response, tr.evidence = scenario.prompt_template, "", {"provider": provider_name, "error": str(exc)}
            db.commit()
        return "FAILED"
    finally:
        db.close()

def execute_campaign(campaign_id):
    db = SessionLocal()
    try:
        campaign = db.get(Campaign, campaign_id)
        if not campaign: return
        cfg = db.get(TestConfiguration, campaign.config_id)
        target = db.get(Target, cfg.target_id)
        strategy = db.get(Strategy, cfg.strategy_id)
        providers = db.query(Provider).filter(Provider.id.in_(cfg.provider_ids), Provider.enabled.is_(True)).all()
        scenarios = db.query(Scenario).filter(Scenario.id.in_(cfg.scenario_ids), Scenario.enabled.is_(True)).all()
        attempts = max(1, cfg.attempts)
        if strategy and strategy.config.get("max_attempts"): attempts = min(attempts, int(strategy.config["max_attempts"]))
        jobs = [(p.name, s, a) for p in providers for s in scenarios for a in range(1, attempts + 1)]
        campaign.total_tests, campaign.completed_tests, campaign.status = len(jobs), 0, "RUNNING"; db.commit()
        strategy_config = strategy.config if strategy else {}
        parallel = bool(strategy_config.get("parallel")); workers = min(8, max(1, len(jobs))) if parallel else 1
        if workers == 1:
            for p, s, a in jobs:
                _execute_one(campaign_id, target.endpoint, p, s, a, strategy_config)
                db.refresh(campaign); campaign.completed_tests += 1; db.commit()
        else:
            with ThreadPoolExecutor(max_workers=workers) as pool:
                futures = [pool.submit(_execute_one, campaign_id, target.endpoint, p, s, a, strategy_config) for p,s,a in jobs]
                for f in as_completed(futures):
                    f.result(); db.refresh(campaign); campaign.completed_tests += 1; db.commit()
        campaign.status = "COMPLETED"; db.commit()
    except Exception as exc:
        campaign = db.get(Campaign, campaign_id)
        if campaign:
            campaign.status = "FAILED"; db.commit()
    finally: db.close()
