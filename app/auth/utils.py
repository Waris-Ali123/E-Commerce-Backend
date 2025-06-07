from passlib.context import CryptContext

from jose import jwt
from datetime import datetime, timedelta


SECRET_KEY = "NAJAN@783@#"
ALGORITHM = "HS256"


def jwt_token_creation(user:dict):
    expiration = datetime.utcnow() + timedelta(days=1)
    jwtContent = {
        "sub": user["sub"],
        "exp": expiration,
        "role": user["role"]
    }
    jwt_encoded = jwt.encode(jwtContent, SECRET_KEY, algorithm=ALGORITHM)
    return jwt_encoded









password_context = CryptContext(schemes=["bcrypt"], deprecated="auto")



def hash_password(password: str) -> str:
    return password_context.hash(password)



def verify_password(plain_password: str, hashed_password: str) -> bool:
    return password_context.verify(plain_password, hashed_password)

