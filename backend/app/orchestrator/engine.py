from concurrent.futures import ThreadPoolExecutor, as_completed
import httpx
from app.database import SessionLocal
from app.models import Provider, Scenario, TestConfiguration, Campaign, TestRun, Target, Strategy


def _execute_one(campaign_id, target_endpoint, provider_name, scenario, attempt):
    db = SessionLocal()
    try:
        tr = TestRun(campaign_id=campaign_id, provider=provider_name, scenario=scenario.key,
                     attempt=attempt, status="RUNNING")
        db.add(tr); db.commit(); db.refresh(tr)
        request = scenario.prompt_template
        try:
            url = target_endpoint.rstrip("/") + "/chat"
            r = httpx.post(url, json={"message": request}, timeout=10)
            data = r.json()
            tr.success = bool(data.get("risk_signal"))
            tr.severity = scenario.severity if tr.success else "INFO"
            tr.evidence = {"risk_signal": data.get("risk_signal"), "target_response": data}
            tr.response = r.text
            tr.status = "COMPLETED"
        except Exception as exc:
            tr.status = "FAILED"; tr.success = False; tr.severity = "INFO"
            tr.evidence = {"error": str(exc)}; tr.response = ""
        tr.request = request
        db.commit()
        return tr.status
    finally:
        db.close()


def execute_campaign(campaign_id):
    db = SessionLocal()
    try:
        campaign = db.get(Campaign, campaign_id)
        if not campaign:
            return
        cfg = db.get(TestConfiguration, campaign.config_id)
        target = db.get(Target, cfg.target_id)
        strategy = db.get(Strategy, cfg.strategy_id)
        providers = db.query(Provider).filter(Provider.id.in_(cfg.provider_ids), Provider.enabled.is_(True)).all()
        scenarios = db.query(Scenario).filter(Scenario.id.in_(cfg.scenario_ids), Scenario.enabled.is_(True)).all()
        attempts = max(1, cfg.attempts)
        if strategy and strategy.config.get("max_attempts"):
            attempts = min(attempts, int(strategy.config["max_attempts"]))
        jobs = [(p.name, s, a) for p in providers for s in scenarios for a in range(1, attempts + 1)]
        campaign.total_tests = len(jobs)
        campaign.completed_tests = 0
        campaign.status = "RUNNING"
        db.commit()
        parallel = bool(strategy and strategy.config.get("parallel"))
        workers = min(8, max(1, len(jobs))) if parallel else 1
        if workers == 1:
            for provider_name, scenario, attempt in jobs:
                _execute_one(campaign_id, target.endpoint, provider_name, scenario, attempt)
                db.refresh(campaign); campaign.completed_tests += 1; db.commit()
        else:
            with ThreadPoolExecutor(max_workers=workers) as pool:
                futures = [pool.submit(_execute_one, campaign_id, target.endpoint, p, s, a) for p, s, a in jobs]
                for future in as_completed(futures):
                    future.result()
                    db.refresh(campaign); campaign.completed_tests += 1; db.commit()
        campaign.status = "COMPLETED"
        db.commit()
    except Exception:
        campaign = db.get(Campaign, campaign_id)
        if campaign:
            campaign.status = "FAILED"; db.commit()
    finally:
        db.close()
