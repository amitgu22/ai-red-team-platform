from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import Provider
from app.schemas import ProviderCreate, ProviderRead

router = APIRouter(prefix="/providers", tags=["providers"])


@router.get("", response_model=list[ProviderRead])
def list_providers(db: Session = Depends(get_db)):
    return db.query(Provider).order_by(Provider.name).all()


@router.post("", response_model=ProviderRead)
def create_provider(payload: ProviderCreate, db: Session = Depends(get_db)):
    provider = Provider(**payload.model_dump())
    db.add(provider)
    db.commit()
    db.refresh(provider)
    return provider


@router.post("/seed")
def seed_providers(db: Session = Depends(get_db)):
    defaults = [
        ("Promptfoo", "container", ["jailbreak", "prompt-injection", "data-leakage"], ["batch"]),
        ("PyRIT", "container", ["jailbreak", "prompt-injection", "adaptive", "multi-turn"], ["batch", "multi-turn", "adaptive"]),
        ("Garak", "container", ["jailbreak", "prompt-injection", "data-leakage", "hallucination"], ["batch"]),
        ("Striker", "container", ["prompt-injection", "agent", "tool-abuse"], ["batch", "agent"]),
    ]
    added = 0
    for name, ptype, caps, modes in defaults:
        if not db.query(Provider).filter_by(name=name).first():
            db.add(Provider(
                name=name,
                provider_type=ptype,
                capabilities=caps,
                execution_modes=modes,
                enabled=True,
            ))
            added += 1
    db.commit()
    return {"added": added}
