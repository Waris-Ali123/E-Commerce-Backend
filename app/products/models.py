from sqlalchemy import Column, Integer, String, Enum as sqlEnum, ForeignKey,Boolean
from app.core.database import Base
from enum import Enum
from sqlalchemy.orm import relationship


class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    description = Column(String, index=True)
    price = Column(Integer, nullable=False)
    stock = Column(Integer, nullable=False)
    category = Column(String, index=True)
    image_url = Column(String, index=True)
    admin_id = Column(Integer,ForeignKey("users.id",ondelete="CASCADE"), nullable=False)
    is_deleted = Column(Boolean,default=False,nullable=False)


    admin = relationship("User", back_populates="products")
    

    carts = relationship("Cart",back_populates="product")
    order_items = relationship("OrderItem",back_populates="product")

    def __str__(self):
        return f"<Product(name={self.name}, price={self.price}, stock={self.stock} , is_deleted={self.is_deleted})>"





#this all imported bcz it is needed by the seeders of our project
from app.auth.models import User 
from app.cart.models import Cart
from app.orders.models import Order
from app.orders.models import OrderItem