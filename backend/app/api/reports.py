from fastapi import APIRouter,Depends,HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import Campaign,Finding,TestRun
router=APIRouter(prefix="/reports",tags=["reports"])
@router.get("/{campaign_id}")
def report(campaign_id:int,db:Session=Depends(get_db)):
 c=db.get(Campaign,campaign_id)
 if not c: raise HTTPException(404,"Campaign not found")
 fs=db.query(Finding).filter_by(campaign_id=campaign_id).order_by(Finding.risk_score.desc()).all()
 runs=db.query(TestRun).filter_by(campaign_id=campaign_id).all()
 return {"generated_at": __import__("datetime").datetime.utcnow().isoformat()+"Z","campaign":{"id":c.id,"name":c.name,"status":c.status,"total_tests":c.total_tests,"completed_tests":c.completed_tests},"summary":{"findings":len(fs),"critical":sum(x.severity=="CRITICAL" for x in fs),"high":sum(x.severity=="HIGH" for x in fs),"medium":sum(x.severity=="MEDIUM" for x in fs),"low":sum(x.severity=="LOW" for x in fs),"pass_count":sum(x.success is False for x in runs)},"findings":[{"id":x.id,"title":x.title,"severity":x.severity,"risk_score":x.risk_score,"confidence":x.confidence,"category":x.category,"mitre_atlas":x.mitre_atlas,"owasp_llm":x.owasp_llm,"impact":x.impact,"recommendation":x.recommendation,"evidence":x.evidence} for x in fs]}
