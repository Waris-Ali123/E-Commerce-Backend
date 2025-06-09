from app.core.database import Base
from sqlalchemy import Integer,Column,String,ForeignKey

class Cart(Base):
    __tablename__ = "carts"

    id = Column(Integer,primary_key = True,index = True)
    user_id = Column(Integer, ForeignKey("users.id",ondelete="CASCADE"),nullable = False)
    product_id = Column(Integer, ForeignKey("products.id",ondelete="CASCADE"),nullable = False)
    quantity = Column(Integer,default=1,nullable=False)


    def __str__(self):
        return f" id : {self.id} , user_id : {self.user_id}, product_id : {self.product_id} and quantity : {self.quantity}"