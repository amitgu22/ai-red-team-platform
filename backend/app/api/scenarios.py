from fastapi import APIRouter,Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import Scenario
from app.schemas import ScenarioRead
router=APIRouter(prefix="/scenarios",tags=["scenarios"])
@router.get("",response_model=list[ScenarioRead])
def list_scenarios(db:Session=Depends(get_db)): return db.query(Scenario).all()
