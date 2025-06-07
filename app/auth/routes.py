from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.database import get_db

from app.auth.crud import signup as signup_service
from app.auth.schemas import UserCreate

router = APIRouter()


@router.post("/signup") 
def signup(user: UserCreate, db : Session = Depends(get_db)):
    signup_response = signup_service(user, db)
    return signup_response