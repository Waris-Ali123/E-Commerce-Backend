from sqlalchemy import Column, Integer, String, Enum as sqlEnum
from app.core.database import Base
from enum import Enum
from sqlalchemy.orm import relationship


#Enum class for user roles
class UserRole(str,Enum):
    USER = "USER"
    ADMIN = "ADMIN"




class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    email = Column(String, unique=True, index=True)
    password = Column(String)
    role = Column(sqlEnum(UserRole), default=UserRole.USER, nullable=False) 

    products = relationship("Product", back_populates="admin")

