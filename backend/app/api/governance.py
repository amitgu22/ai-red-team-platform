from datetime import datetime
import csv, io
from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session
from sqlalchemy import func
from app.database import get_db
from app.models import Campaign, Finding, Scenario, TestRun, Remediation

router=APIRouter(prefix="/governance",tags=["governance"])

@router.get("/risk-register")
def risk_register(status:str|None=None,db:Session=Depends(get_db)):
    q=db.query(Finding).order_by(Finding.risk_score.desc(),Finding.id.desc())
    if status: q=q.filter(Finding.status==status.upper())
    rows=[]
    for f in q.all():
        r=db.query(Remediation).filter_by(finding_id=f.id).first()
        rows.append({"finding_id":f.id,"title":f.title,"severity":f.severity,"risk_score":f.risk_score,"confidence":f.confidence,"category":f.category,"status":f.status,"owner":r.owner if r else None,"due_date":r.due_date.isoformat() if r and r.due_date else None,"remediation_status":r.status if r else "NOT_STARTED","recommendation":f.recommendation})
    return rows

@router.put("/risk-register/{finding_id}")
def update_risk(finding_id:int, payload:dict, db:Session=Depends(get_db)):
    f=db.get(Finding,finding_id)
    if not f: raise HTTPException(404,"Finding not found")
    if "status" in payload: f.status=str(payload["status"]).upper()
    r=db.query(Remediation).filter_by(finding_id=f.id).first()
    if not r: r=Remediation(finding_id=f.id); db.add(r)
    for key in ("owner","notes","status"):
        if key in payload and payload[key] is not None:
            setattr(r, key if key!="status" else "status", str(payload[key]).upper() if key=="status" else payload[key])
    if payload.get("due_date"):
        r.due_date=datetime.fromisoformat(payload["due_date"].replace("Z","+00:00")).replace(tzinfo=None)
    db.commit(); return {"finding_id":f.id,"status":f.status,"remediation_status":r.status,"owner":r.owner,"due_date":r.due_date.isoformat() if r.due_date else None}

@router.get("/coverage")
def coverage(db:Session=Depends(get_db)):
    scenarios=db.query(Scenario).filter_by(enabled=True).all()
    runs=db.query(TestRun).all()
    covered={r.scenario for r in runs}
    bycat={}
    for s in scenarios:
        x=bycat.setdefault(s.category,{"category":s.category,"total":0,"tested":0,"findings":0})
        x["total"]+=1; x["tested"]+=int(s.key in covered)
    findings=db.query(Finding).all()
    for f in findings:
        if f.category in bycat: bycat[f.category]["findings"]+=1
    for x in bycat.values(): x["coverage_pct"]=round(x["tested"]/x["total"]*100,1) if x["total"] else 0
    return {"total_scenarios":len(scenarios),"tested_scenarios":len(covered & {s.key for s in scenarios}),"coverage_pct":round(len(covered & {s.key for s in scenarios})/len(scenarios)*100,1) if scenarios else 0,"categories":list(bycat.values())}

@router.get("/trends")
def trends(db:Session=Depends(get_db)):
    campaigns=db.query(Campaign).order_by(Campaign.created_at.asc()).all()
    out=[]
    for c in campaigns:
        fs=db.query(Finding).filter_by(campaign_id=c.id).all(); runs=db.query(TestRun).filter_by(campaign_id=c.id).all()
        out.append({"campaign_id":c.id,"campaign":c.name,"created_at":c.created_at.isoformat(),"tests":len(runs),"findings":len(fs),"critical":sum(f.severity=="CRITICAL" for f in fs),"high":sum(f.severity=="HIGH" for f in fs),"avg_risk":round(sum(f.risk_score for f in fs)/len(fs),1) if fs else 0})
    return out

@router.get("/export.csv")
def export_csv(db:Session=Depends(get_db)):
    output=io.StringIO(); w=csv.writer(output); w.writerow(["Finding ID","Title","Severity","Risk Score","Confidence","Category","Status","Recommendation"])
    for f in db.query(Finding).order_by(Finding.risk_score.desc()).all(): w.writerow([f.id,f.title,f.severity,f.risk_score,f.confidence,f.category,f.status,f.recommendation])
    output.seek(0); return StreamingResponse(iter([output.getvalue()]),media_type="text/csv",headers={"Content-Disposition":"attachment; filename=ai-red-team-risk-register.csv"})
