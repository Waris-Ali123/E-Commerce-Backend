from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt
from jose import JWTError
import logging


from .utils import SECRET_KEY, ALGORITHM

from app.auth.models import User, UserRole
from app.core.database import get_db


tokenOrigin = OAuth2PasswordBearer(tokenUrl="signin")


#Create a logger
logger = logging.getLogger(__name__)

def get_current_user(token: str = Depends(tokenOrigin), db=Depends(get_db)):
    try:
        logger.info("Decoding JWT token")
        decoded_jwt = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_email = decoded_jwt.get("sub")
        if user_email is None:
            logger.error("JWT token does not contain user email")
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Jwt token does not contain user email."
            )
        user = db.query(User).filter(User.email == user_email).first()
        if user is None:
            logger.error(f"User with email {user_email} not found")
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="User not found."
            )
        return user.__dict__  # Convert SQLAlchemy model to dict for easier access
    except jwt.JWTError:
        logger.error("JWT token is invalid or expired")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Jwt token is invalid or expired."
        )
    
def admin_required(current_user: User = Depends(get_current_user)):
    if current_user["role"] != UserRole.ADMIN.value:
        logger.warning(f"Unauthorized access attempt by user: {current_user['email']}")
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only admin can perform this action."
        )
    return current_user




def only_user_allowed(current_user: User = Depends(get_current_user)):
    if current_user["role"] != UserRole.USER.value:
        logger.warning(f"Only users are allowed : {current_user['email']}")
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only User can perform this action."
        )
    return current_user

