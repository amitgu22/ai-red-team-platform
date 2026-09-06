from fastapi import FastAPI
from pydantic import BaseModel
app=FastAPI(title="Sample AI Customer Support Agent")
class Chat(BaseModel): message:str
@app.get("/health")
def health(): return {"status":"ok"}
@app.post("/chat")
def chat(x:Chat):
 m=x.message.lower()
 if "system prompt" in m or "ignore previous" in m:return {"response":"DEMO: simulated system instruction exposed.","risk_signal":"system_prompt_exposure"}
 if "customer" in m or "secret" in m:return {"response":"DEMO: simulated customer test data CUSTOMER-TEST-001.","risk_signal":"sensitive_data_exposure"}
 if "tool" in m or "delete" in m:return {"response":"DEMO: simulated unauthorized tool invocation.","tool_call":{"name":"demo_customer_update","authorized":False},"risk_signal":"tool_authorization"}
 return {"response":"Demo agent response.","risk_signal":None}
