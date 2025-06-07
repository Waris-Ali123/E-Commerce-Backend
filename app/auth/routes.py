from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.auth.crud import signup as signup_service
from app.auth.schemas import UserCreate
from app.auth.permissions import admin_required

router = APIRouter()


@router.post("/signup") 
def signup(user: UserCreate, db : Session = Depends(get_db)):
    signup_response = signup_service(user, db)
    return signup_response

@router.get("/users")
def show_all_users(db: Session = Depends(get_db),
                   current_user: dict = Depends(admin_required)):
    from app.auth.crud import show_all_users as  show_all_users_service
    users = show_all_users_service(db)
    return users


@router.get("/signin")
def signin(email: str, password: str, db: Session = Depends(get_db)):
    from app.auth.crud import signin as signin_service
    signin_response = signin_service(email, password, db)
    return signin_response


@router.delete("/delete/{user_id}")
def delete_user(user_id: int, db: Session = Depends(get_db),
                current_user: dict = Depends(admin_required)):
    from app.auth.crud import delete_user as delete_user_service
    delete_response = delete_user_service(user_id, db)
    return delete_response