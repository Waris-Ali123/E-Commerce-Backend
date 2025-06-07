from app.auth.models import User
from app.auth.utils import hash_password,verify_password, jwt_token_creation


def signup(user, db):

    # print("Session Local:", db)

    db_user = db.query(User).filter(User.email == user.email).first()
    if db_user:
        return {"message": "User already exists with this email."}
    user_to_store = User(
        name=user.full_name,
        email=user.email,
        password=hash_password(user.password),
        role=user.role
    )
    db.add(user_to_store)
    db.commit()
    db.refresh(user_to_store)
    return {"User" : user_to_store, 
            "message": "User created successfully."}



def show_all_users(db):
    users = db.query(User).all()
    return users



def signin(email: str, password: str, db):
    user = db.query(User).filter(User.email == email).first()
    if not user:
        return {"message": "User not found."}
    
    if not verify_password(password, user.password):
        return {"message": "Incorrect password."}
    
    # Generate JWT token
    token_data = {"sub": user.email, "role": user.role}
    access_token = jwt_token_creation(token_data)
    
    return {
        "message": "Login successful.",
        "access_token": access_token,
        "token_type": "bearer",
        "user": user
    }
    
    # return {"message": "Login successful.", "user": user}


