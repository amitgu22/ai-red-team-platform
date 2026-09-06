from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import TestConfiguration, Target, Provider, Scenario, Strategy
from app.schemas import TestConfigCreate, TestConfigRead

router = APIRouter(prefix="/test-configurations", tags=["test-configurations"])

@router.get("", response_model=list[TestConfigRead])
def list_configs(db: Session = Depends(get_db)):
    return db.query(TestConfiguration).order_by(TestConfiguration.id.desc()).all()

@router.post("", response_model=TestConfigRead)
def create_config(p: TestConfigCreate, db: Session = Depends(get_db)):
    target = db.get(Target, p.target_id)
    strategy = db.get(Strategy, p.strategy_id)
    providers = db.query(Provider).filter(Provider.id.in_(p.provider_ids), Provider.enabled.is_(True)).all()
    scenarios = db.query(Scenario).filter(Scenario.id.in_(p.scenario_ids), Scenario.enabled.is_(True)).all()
    if not target or not target.enabled: raise HTTPException(400, "Target is not available")
    if not strategy: raise HTTPException(400, "Strategy not found")
    if len(providers) != len(set(p.provider_ids)): raise HTTPException(400, "One or more providers are invalid or disabled")
    if len(scenarios) != len(set(p.scenario_ids)): raise HTTPException(400, "One or more scenarios are invalid or disabled")
    if p.attempts < 1 or p.attempts > 20: raise HTTPException(400, "Attempts must be between 1 and 20")
    x = TestConfiguration(**p.model_dump())
    db.add(x); db.commit(); db.refresh(x); return x
