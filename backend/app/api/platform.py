from fastapi import APIRouter, Depends, HTTPException, Request
from pydantic import BaseModel
from sqlalchemy import select, desc
from app.auth import require_role
from app.database import SessionLocal
from app.models import AuditLog, Policy, Schedule
from datetime import datetime

router=APIRouter(prefix='/platform',tags=['platform'])

class PolicyIn(BaseModel):
    name:str; description:str=''; rules:dict={}; enabled:bool=True
class ScheduleIn(BaseModel):
    name:str; config_id:int; cron:str; enabled:bool=True

@router.get('/audit', dependencies=[Depends(require_role('admin','auditor'))])
def audit(limit:int=100):
    with SessionLocal() as db:
        rows=db.scalars(select(AuditLog).order_by(desc(AuditLog.created_at)).limit(min(limit,500))).all()
        return [{'id':r.id,'actor':r.actor,'role':r.role,'action':r.action,'resource':r.resource,'method':r.method,'status_code':r.status_code,'metadata':r.audit_metadata,'created_at':r.created_at.isoformat()} for r in rows]

@router.get('/policies')
def policies():
    with SessionLocal() as db:
        return db.scalars(select(Policy).order_by(Policy.name)).all()

@router.post('/policies', dependencies=[Depends(require_role('admin'))])
def create_policy(payload:PolicyIn):
    with SessionLocal() as db:
        if db.scalar(select(Policy).where(Policy.name==payload.name)): raise HTTPException(409,'Policy already exists')
        p=Policy(**payload.model_dump()); db.add(p); db.commit(); db.refresh(p); return p

@router.post('/schedules', dependencies=[Depends(require_role('admin'))])
def create_schedule(payload:ScheduleIn):
    if not payload.cron.strip(): raise HTTPException(400,'cron is required')
    with SessionLocal() as db:
        s=Schedule(**payload.model_dump()); db.add(s); db.commit(); db.refresh(s); return s

@router.get('/schedules')
def schedules():
    with SessionLocal() as db: return db.scalars(select(Schedule).order_by(Schedule.name)).all()
