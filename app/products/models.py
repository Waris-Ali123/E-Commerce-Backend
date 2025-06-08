from sqlalchemy import Column, Integer, String, Enum as sqlEnum, ForeignKey
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


    admin = relationship("User", back_populates="products")

    def __str__(self):
        return f"<Product(name={self.name}, price={self.price}, stock={self.stock})>"
