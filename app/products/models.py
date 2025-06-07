from sqlalchemy import Column, Integer, String, Enum as sqlEnum
from app.core.database import Base
from enum import Enum


class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    description = Column(String, index=True)
    price = Column(Integer, nullable=False)
    stock = Column(Integer, nullable=False)
    category = Column(String, index=True)
    image_url = Column(String, index=True)

    def __str__(self):
        return f"<Product(name={self.name}, price={self.price}, stock={self.stock})>"
