from pydantic import BaseModel,Field
from sqlalchemy import Integer
from datetime import datetime
from app.auth.schemas import UserOut
from app.products.schemas import ProductOut
from typing import List
# from app.orders.models import OrderItem



class OrderItemOut(BaseModel):


    id : int = Field(...,description="This is order item id")
    order_id : int = Field(...,description="This order id contains this order item")
    product_id : int = Field(...,description="This is the product id")
    product : ProductOut = Field(... ,description="Product Complete detials")
    quantity : int = Field(...,description="This much quantity has ordered")
    price_at_purchase : float = Field(...,description="This was the price when ordered")



    class Config:
        orm_mode = True
        allow_population_by_field_name = True




class OrderOutBase(BaseModel):

    id : int = Field(...,description="This is id of order")
    user_id : int = Field(...,description="This is user id")
    total_amount : int = Field(...,description="This is total amount of order")
    status : str = Field(...,description="This shows the status whether pending, paid or cancelled")
    created_at : datetime = Field(...,description="This the time when the order was placed")
    user : UserOut = Field(...,description="User details")

    class Config:
        orm_mode = True
        allow_population_by_field_name = True

class OrderOutWithOrderItems(OrderOutBase):

    order_items : List[OrderItemOut] = Field(...,description="All items that the order includes")



class OrderOutWithoutOrderItems(OrderOutBase):
    pass