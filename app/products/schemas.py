from pydantic import BaseModel
from pydantic import Field
from app.auth.schemas import UserOut



class ProductCreate(BaseModel):
    name: str = Field(..., description="The name of the product")
    description: str = Field(..., description="The full description of the product")
    price: float = Field(..., description="The price of the product")
    stock: int = Field(..., description="The stock quantity of the product")
    category: str = Field(..., description="The category of the product")
    image_url: str = Field(..., description="The image URL of the product")





class ProductOut(BaseModel):
    id: int = Field(..., description="The unique identifier of the product")
    name: str = Field(..., description="The name of the product")
    description: str = Field(..., description="The full description of the product")
    price: float = Field(..., description="The price of the product")
    stock: int = Field(..., description="The stock quantity of the product")
    category: str = Field(..., description="The category of the product")
    image_url: str = Field(..., description="The image URL of the product")
    admin_id: int = Field(..., description="The ID of the admin who created the product")
    admin : UserOut = Field(..., description="The admin who created the product")

    class Config:
        orm_mode = True