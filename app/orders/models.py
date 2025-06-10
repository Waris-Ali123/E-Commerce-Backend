from sqlalchemy import Column,Integer,Float,Enum as SqlEnum,ForeignKey,DateTime
from app.core.database import Base
from enum import Enum
from datetime import datetime
from sqlalchemy.orm import relationship


class Status(Enum):

    PENDING = "PENDING"
    PAID = "PAID"
    CANCELLED = "CANCELLED"




class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer,index=True,primary_key=True)
    user_id = Column(Integer,ForeignKey(column="users.id",ondelete="CASCADE"),nullable=False)
    total_amount = Column(Float,nullable=False)
    status = Column(SqlEnum(Status),default=Status.PENDING,nullable=False)
    created_at = Column(DateTime,default= datetime.now(),nullable=False)

    order_items = relationship("OrderItem",back_populates="order")
    user = relationship("User",back_populates="orders")

    def __str__(self):
        return f"Order with id : {self.id} by user id : {self.user_id} having total as : {self.total_amount} and status as {self.status} created at {self.created_at} owns following {self.order_items}"


class OrderItem(Base):
    __tablename__ = "order_items"

    id = Column(Integer,index=True,primary_key=True)
    order_id = Column(Integer,ForeignKey("orders.id",ondelete="CASCADE"),nullable=True)
    product_id = Column(Integer,ForeignKey("products.id"),nullable=False)
    quantity = Column(Integer,nullable=False)
    price_at_purchase = Column(Float,nullable=True)

    order = relationship("Order",back_populates="order_items")
    product = relationship("Product",back_populates="order_items")

    def __str__(self):
        return f"Order Item \n id : {self.id} || order_id : {self.order_id} || product_id : {self.product_id} || quantity : {self.quantity} || price_at_purchase : {self.price_at_purchase}"