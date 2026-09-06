from fastapi import APIRouter,Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import Strategy
from app.schemas import StrategyRead
router=APIRouter(prefix="/strategies",tags=["strategies"])
@router.get("",response_model=list[StrategyRead])
def list_strategies(db:Session=Depends(get_db)): return db.query(Strategy).all()
