from fastapi import APIRouter,Depends,HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func
from app.database import get_db
from app.models import Finding,Campaign
from app.schemas import FindingRead,RiskSummary
router=APIRouter(prefix="/findings",tags=["findings"])
@router.get("",response_model=list[FindingRead])
def list_findings(campaign_id:int|None=None,status:str|None=None,db:Session=Depends(get_db)):
 q=db.query(Finding)
 if campaign_id is not None:q=q.filter_by(campaign_id=campaign_id)
 if status:q=q.filter_by(status=status.upper())
 return q.order_by(Finding.risk_score.desc(),Finding.id.desc()).all()
@router.get("/summary",response_model=RiskSummary)
def summary(campaign_id:int|None=None,db:Session=Depends(get_db)):
 q=db.query(Finding)
 if campaign_id is not None:q=q.filter_by(campaign_id=campaign_id)
 xs=q.all(); n=len(xs)
 return RiskSummary(total=n,critical=sum(x.severity=="CRITICAL" for x in xs),high=sum(x.severity=="HIGH" for x in xs),medium=sum(x.severity=="MEDIUM" for x in xs),low=sum(x.severity=="LOW" for x in xs),average_score=round(sum(x.risk_score for x in xs)/n,1) if n else 0,open=sum(x.status=="OPEN" for x in xs))
@router.get("/{finding_id}",response_model=FindingRead)
def get_finding(finding_id:int,db:Session=Depends(get_db)):
 x=db.get(Finding,finding_id)
 if not x: raise HTTPException(404,"Finding not found")
 return x
