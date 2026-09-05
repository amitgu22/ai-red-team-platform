from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.database import init_db
from app.api import health, providers, targets

app = FastAPI(
    title="AI Red Team Platform",
    version="0.1.0",
    description="Vendor-neutral AI red teaming platform — Phase 1 POC",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(health.router, prefix="/api")
app.include_router(providers.router, prefix="/api")
app.include_router(targets.router, prefix="/api")


@app.on_event("startup")
def startup():
    init_db()
