from sqlalchemy import Column, Integer, String, Enum as sqlEnum,DateTime,Boolean,ForeignKey
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
    carts = relationship("Cart",back_populates="user")
    orders = relationship("Order",back_populates="user")

    

class PasswordResetToken(Base):
    __tablename__ = "password_reset_tokens"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer,ForeignKey("users.id",ondelete="CASCADE"), nullable=False)
    token = Column(String,nullable=False)
    expiration_time = Column(DateTime,nullable=False)
    used = Column(Boolean,nullable=False,default=False)


    def __str__(self):
        return f"User id : {self.user_id} || Used : {self.used} || Expriation time : {self.expiration_time}"

    
    