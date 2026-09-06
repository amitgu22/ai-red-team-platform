from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import Provider, Target

router = APIRouter(tags=["catalog"])

@router.get("/providers")
def list_providers(db: Session = Depends(get_db)):
    return db.query(Provider).order_by(Provider.name).all()

@router.get("/targets")
def list_targets(db: Session = Depends(get_db)):
    return db.query(Target).order_by(Target.name).all()
