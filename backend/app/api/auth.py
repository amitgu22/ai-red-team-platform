from fastapi import APIRouter, Depends, Request
from app.auth import authenticate
router=APIRouter(prefix='/auth',tags=['auth'])
@router.get('/me')
def me(request: Request, identity=Depends(authenticate)):
    return identity
