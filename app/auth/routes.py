from fastapi import APIRouter, Depends, Query, Body
from sqlalchemy.orm import Session
from pydantic import EmailStr
from app.core.database import get_db
from app.auth.crud import signup as signup_service
from app.auth.schemas import UserCreate, UserOut,PasswordReset
from app.auth.permissions import admin_required

router = APIRouter()


@router.post("/signup", response_model=UserOut) 
def signup(user: UserCreate, db : Session = Depends(get_db)):
    signup_response = signup_service(user, db)
    print("Signup response:", signup_response)
    return signup_response

@router.get("/users", response_model=list[UserOut])
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



@router.post("/forgot-password")
def forgot_password(email : EmailStr = Query(...),db : Session = Depends(get_db)):
    from app.auth.crud import forgot_password_service
    return forgot_password_service(email,db)


@router.get("/reset-password")
def reset_password(
    password_reset_body : PasswordReset = Body(),
    db:Session = Depends(get_db)):
    from app.auth.crud import reset_password_service
    token = password_reset_body.token
    new_password = password_reset_body.new_password
    return reset_password_service(token,new_password,db)