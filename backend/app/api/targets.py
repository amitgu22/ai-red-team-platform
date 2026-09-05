from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import Target
from app.schemas import TargetCreate, TargetRead

router = APIRouter(prefix="/targets", tags=["targets"])


@router.get("", response_model=list[TargetRead])
def list_targets(db: Session = Depends(get_db)):
    return db.query(Target).order_by(Target.name).all()


@router.post("", response_model=TargetRead)
def create_target(payload: TargetCreate, db: Session = Depends(get_db)):
    target = Target(**payload.model_dump())
    db.add(target)
    db.commit()
    db.refresh(target)
    return target


@router.post("/seed")
def seed_target(db: Session = Depends(get_db)):
    if not db.query(Target).filter_by(name="Sample Customer Support Agent").first():
        db.add(Target(
            name="Sample Customer Support Agent",
            target_type="agent",
            endpoint="http://sample-target:8000",
            capabilities=["chat", "rag", "agent", "tools"],
            description="Local intentionally vulnerable target for authorized security testing.",
        ))
        db.commit()
        return {"added": 1}
    return {"added": 0}
