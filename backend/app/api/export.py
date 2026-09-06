from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import Response
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import Campaign, Finding
router=APIRouter(prefix="/export",tags=["export"])
@router.get("/campaign/{campaign_id}.pdf")
def campaign_pdf(campaign_id:int,db:Session=Depends(get_db)):
    c=db.get(Campaign,campaign_id)
    if not c: raise HTTPException(404,"Campaign not found")
    fs=db.query(Finding).filter_by(campaign_id=campaign_id).order_by(Finding.risk_score.desc()).all()
    from reportlab.lib.pagesizes import A4
    from reportlab.platypus import SimpleDocTemplate,Paragraph,Spacer,Table,TableStyle
    from reportlab.lib.styles import getSampleStyleSheet
    from reportlab.lib import colors
    from reportlab.lib.units import mm
    import io
    buf=io.BytesIO(); doc=SimpleDocTemplate(buf,pagesize=A4,rightMargin=15*mm,leftMargin=15*mm,topMargin=15*mm,bottomMargin=15*mm)
    styles=getSampleStyleSheet(); story=[Paragraph("AI Red Team Executive Risk Report",styles["Title"]),Paragraph(c.name,styles["Heading2"]),Paragraph(f"Status: {c.status} · Tests: {c.completed_tests}/{c.total_tests} · Findings: {len(fs)}",styles["BodyText"]),Spacer(1,8)]
    data=[["Severity","Risk","Confidence","Category","Finding"]]+[[f.severity,str(f.risk_score),str(f.confidence),f.category,f.title] for f in fs]
    if len(data)==1: data.append(["—","—","—","—","No findings"] )
    t=Table(data,colWidths=[25*mm,20*mm,25*mm,35*mm,70*mm],repeatRows=1); t.setStyle(TableStyle([("BACKGROUND",(0,0),(-1,0),colors.HexColor("#1f2937")),("TEXTCOLOR",(0,0),(-1,0),colors.white),("GRID",(0,0),(-1,-1),.4,colors.grey),("VALIGN",(0,0),(-1,-1),"TOP")])); story.append(t); story.append(Spacer(1,10))
    for f in fs: story += [Paragraph(f"<b>{f.title}</b> — {f.severity}, risk {f.risk_score}",styles["Heading3"]),Paragraph(f"Impact: {f.impact}",styles["BodyText"]),Paragraph(f"Recommendation: {f.recommendation}",styles["BodyText"]),Spacer(1,6)]
    doc.build(story); return Response(buf.getvalue(),media_type="application/pdf",headers={"Content-Disposition":f'attachment; filename="campaign-{campaign_id}-report.pdf"'})
