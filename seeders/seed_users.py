from sqlalchemy.orm import Session
from app.core.database import SessionLocal
from app.auth.schemas import UserCreate
from app.auth.crud import signup
from fastapi import HTTPException
import logging
# Ensure DB tables are created
# Base.metadata.create_all(bind=engine)


logger = logging.getLogger(__name__)
def seed_user(user_data: dict, db: Session):
    try:
        user_schema = UserCreate(**user_data)
        signup(user_schema, db)
        logger.info(f"{user_data['role'].capitalize()} '{user_data['email']}' created successfully.")
    except HTTPException as e:
        if e.status_code == 409:
            logger.error(f"User '{user_data['email']}' already exists.")

        raise e

def main():
    db = SessionLocal()
    try:
        users_to_seed = [
            {
                "full_name": "Admin User",
                "email": "admin@example.com",
                "password": "Admin@123",
                "role": "ADMIN"
            },
            {
                "full_name": "Regular User",
                "email": "user@example.com",
                "password": "User@123",
                "role": "USER"
            }
        ]

        for user_data in users_to_seed:
            seed_user(user_data, db)

    finally:
        db.close()

if __name__ == "__main__":
    main()
