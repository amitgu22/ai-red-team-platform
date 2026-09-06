from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.database import init_db
from app.api import health, scenarios, strategies, testconfigs, campaigns, catalog
app=FastAPI(title="AI Red Team Platform",version="0.2.0")
app.add_middleware(CORSMiddleware,allow_origins=["*"],allow_methods=["*"],allow_headers=["*"])
app.include_router(health.router,prefix="/api")
app.include_router(scenarios.router,prefix="/api")
app.include_router(strategies.router,prefix="/api")
app.include_router(testconfigs.router,prefix="/api")
app.include_router(campaigns.router,prefix="/api")
app.include_router(catalog.router,prefix="/api")
@app.on_event("startup")
def startup(): init_db()
