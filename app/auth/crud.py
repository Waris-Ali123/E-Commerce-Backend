import logging


from app.auth.models import User
from app.auth.utils import hash_password,verify_password, jwt_token_creation
from app.auth.schemas import UserOut


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
        logger.warning(f"User with email {user.email} already exists.")
        return {"message": "User already exists with this email."}
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
        logger.info("No users found in the database.")
        return {"message": "No users found."}
    return users



def signin(email: str, password: str, db):
    logger.info(f"Attempting to sign in user with email: {email}")
    user = db.query(User).filter(User.email == email).first()
    if not user:
        logger.warning(f"User with email {email} not found.")
        return {"message": "User not found."}
    
    if not verify_password(password, user.password):
        logger.warning(f"Incorrect password for user with email: {email}")
        return {"message": "Incorrect password."}
    
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
        logger.warning(f"User with ID {user_id} not found.")
        return {"message": "User not found."}
    
    db.delete(user)
    db.commit()
    logger.info(f"User with ID {user_id} deleted successfully.")
    return {"message": "User deleted successfully."}