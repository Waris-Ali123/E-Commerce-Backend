import logging

from fastapi import HTTPException,status
from app.auth.models import User,PasswordResetToken
from app.auth.utils import hash_password,verify_password, jwt_token_creation
from app.auth.schemas import UserOut
from sqlalchemy.orm import Session
from datetime import datetime, timedelta




#creating logger
logger = logging.getLogger(__name__)
logging.basicConfig(
    level=logging.INFO,  # or DEBUG for even more logs
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s"
)

def signup(user, db):

    # print("Session Local:", db)

    db_user = db.query(User).filter(User.email == user.email).first()
    if db_user:
        # logger.warning(f"User with email {user.email} already exists.")
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,detail=f"User with email {user.email} already exists.")
    user_to_store = User(
        name=user.full_name,
        email=user.email,
        password=hash_password(user.password),
        role=user.role
    )

    logger.info(f"Creating user with email : {user_to_store.email}")
    # print("User to store:", user_to_store)
    db.add(user_to_store)
    db.commit()
    db.refresh(user_to_store)
    logger.info(f"User created successfully with email: {user_to_store.email}")
    return user_to_store



def show_all_users(db):
    users = db.query(User).all()
    if not users:
        # logger.info("No users found in the database.")
        # return {"message": "No users found."}
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="No user found in the database")
    return users



def signin(email: str, password: str, db):
    logger.info(f"Attempting to sign in user with email: {email}")
    user = db.query(User).filter(User.email == email).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"No User found for email : {email}")
    
    if not verify_password(password, user.password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail=f"Invalid Password")
    
    # Generate JWT token
    logger.info(f"User {email} has put correct password, generating JWT token.")

    token_data = {"sub": user.email, "role": user.role}
    access_token = jwt_token_creation(token_data)

    logger.info(f"JWT token generated for user {email}.")

    userOut = UserOut.from_orm(user)
    
    return {
        "message": "Login successful.",
        "access_token": access_token,
        "token_type": "bearer",
        "user": userOut
    }
    


def delete_user(user_id: int, db):
    logger.info(f"Attempting to delete user with ID: {user_id}")
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"No User found for email : {email}")

    
    db.delete(user)
    db.commit()
    logger.info(f"User with ID {user_id} deleted successfully.")
    return {"message": "User deleted successfully."}



def forgot_password_service(email_coming,db:Session):
    from app.core.config import settings
    from app.utils.email_sender import sending_email_with_token
    import secrets

    existing_user = db.query(User).filter(User.email == email_coming).first()

    if not existing_user:
        # logger.warning(f"User not found with email {email_coming}")
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"User not found with email {email_coming}")
    

    logger.info(f"Generating token for {email_coming}")
    token_by_secret = secrets.token_urlsafe(32)
    new_reset_token_entry = PasswordResetToken(
        user_id = existing_user.id,
        token = token_by_secret,
        expiration_time = datetime.utcnow() + timedelta(minutes=5), 
        used = False
    )

    db.add(new_reset_token_entry)
    db.commit()
    db.refresh(new_reset_token_entry)

    sender = settings.EMAIL_USER
    password = settings.EMAIL_PASS
    receiver = existing_user.email
    receiver_name = existing_user.name
    reset_token = new_reset_token_entry.token

    sending_email_with_token(sender=sender,password=password,receiver=receiver,reset_token=reset_token,receiver_name=receiver_name)

    return new_reset_token_entry



def reset_password_service(token_coming,new_password,db):
    
    reset_token_entry = db.query(PasswordResetToken).filter(PasswordResetToken.token == token_coming).first()

    if (not reset_token_entry) or (reset_token_entry.used) or (reset_token_entry.expiration_time < datetime.utcnow()):
        logger.error("Invalid Token or Used earlier or time expired")
        if (not reset_token_entry):
            logger.warning(f"no reset token found for {token_coming}")
        elif reset_token_entry.used:
            logger.warning(f"reset token has already used")
        else:
            logger.warning(f"expired")
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail="Invalid Token or Used earlier or time expired")

    user = db.query(User).filter(User.id == reset_token_entry.user_id).first()

    user.password = hash_password(new_password)

    reset_token_entry.used = True

    db.commit()

    db.refresh(reset_token_entry)
    print(reset_token_entry)

    return {"msg" : "Password has been reset successfully"}
