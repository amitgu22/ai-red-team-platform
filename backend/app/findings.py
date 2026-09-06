import hashlib
from app.database import SessionLocal
from app.models import TestRun, Scenario, Finding

SEV={"CRITICAL":95,"HIGH":80,"MEDIUM":55,"LOW":25,"INFO":10}
MAP={
 "prompt-injection":(["AML.T0051"],["LLM01"],"Instruction override can redirect model behavior or bypass intended controls."),
 "data-leakage":(["AML.T0057"],["LLM06"],"Sensitive information may be disclosed to an unauthorized requester."),
 "jailbreak":(["AML.T0054"],["LLM01"],"Safety or policy controls may be bypassed through adversarial prompting."),
 "tool-abuse":(["AML.T0052"],["LLM07"],"Unauthorized tool use can cause unintended external side effects."),
}
RECS={"prompt-injection":"Enforce trusted/untrusted context separation, instruction hierarchy, input scanning and adversarial regression tests.","data-leakage":"Apply least privilege, output DLP/PII filtering, retrieval authorization and canary secrets.","jailbreak":"Strengthen policy enforcement, layered moderation and continuous jailbreak evaluation.","tool-abuse":"Require explicit tool authorization, allowlists, parameter validation and human approval for destructive actions."}
def build_finding(tr, scenario):
 cat=scenario.category; base=SEV.get(scenario.severity,20); evidence=tr.evidence or {};
 success=bool(tr.success)
 if not success: return None
 atlas,owasp,impact=MAP.get(cat,([],[],"Adversarial behavior was detected."))
 score=min(100,base + (5 if tr.attempt>1 else 0))
 fp=hashlib.sha256(f"{cat}|{scenario.key}|{tr.provider}".encode()).hexdigest()[:32]
 return Finding(test_run_id=tr.id,campaign_id=tr.campaign_id,title=scenario.name, fingerprint=fp,severity=scenario.severity,risk_score=score,confidence=0.85 if evidence else 0.65,category=cat,mitre_atlas=atlas,owasp_llm=owasp,impact=impact,recommendation=RECS.get(cat,"Review the evidence and add a targeted control."),evidence=evidence,status="OPEN")
def generate_for_campaign(campaign_id):
 db=SessionLocal()
 try:
  runs=db.query(TestRun).filter_by(campaign_id=campaign_id).all(); created=0
  for tr in runs:
   if db.query(Finding).filter_by(test_run_id=tr.id).first(): continue
   sc=db.query(Scenario).filter_by(key=tr.scenario).first()
   if not sc: continue
   x=build_finding(tr,sc)
   if x: db.add(x); created+=1
  db.commit(); return created
 finally: db.close()
