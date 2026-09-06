from fastapi import APIRouter, Depends, HTTPException
from fastapi.background import BackgroundTasks
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import Campaign, TestConfiguration, TestRun
from app.schemas import CampaignCreate, CampaignRead, TestRunRead
from app.orchestrator.engine import execute_campaign

router = APIRouter(prefix="/campaigns", tags=["campaigns"])

@router.get("", response_model=list[CampaignRead])
def list_campaigns(db: Session = Depends(get_db)):
    return db.query(Campaign).order_by(Campaign.id.desc()).all()

@router.post("", response_model=CampaignRead)
def create_campaign(p: CampaignCreate, db: Session = Depends(get_db)):
    cfg = db.get(TestConfiguration, p.config_id)
    if not cfg: raise HTTPException(404, "Configuration not found")
    c = Campaign(name=p.name, config_id=cfg.id, status="QUEUED")
    db.add(c); db.commit(); db.refresh(c); return c

@router.post("/{campaign_id}/start", response_model=CampaignRead)
def start_campaign(campaign_id: int, background_tasks: BackgroundTasks, db: Session = Depends(get_db)):
    c = db.get(Campaign, campaign_id)
    if not c: raise HTTPException(404, "Campaign not found")
    if c.status in {"RUNNING", "COMPLETED"}: return c
    c.status = "QUEUED"; db.commit(); db.refresh(c)
    background_tasks.add_task(execute_campaign, c.id)
    return c

@router.get("/{campaign_id}/runs", response_model=list[TestRunRead])
def runs(campaign_id: int, db: Session = Depends(get_db)):
    return db.query(TestRun).filter_by(campaign_id=campaign_id).order_by(TestRun.id.desc()).all()
