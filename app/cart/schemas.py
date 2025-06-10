from pydantic import BaseModel,Field
# from app.products.models import User
from app.auth.schemas import UserOut
from app.products.schemas import ProductOut

class CartOut(BaseModel):

    id : int = Field(...,description="This tells the card id")
    user_id : int = Field(...,description="This is the id of user created cart")
    product_id : int = Field(...,description="This is the id of product added in cart")
    quantity : int = Field(...,description="This is the quantity of item")
    user : UserOut = Field(..., description="This is complete user detail")
    product : ProductOut = Field(...,description="This is complete detail of product")

    class Config:
        orm_mode = True