from pydantic import BaseModel
from app.orders.schemas import OrderOutWithOrderItems
from app.cart.schemas import CartOut

class CheckoutResponse(BaseModel):
    order : OrderOutWithOrderItems
    msg : str
    deleted_items : list[CartOut]
