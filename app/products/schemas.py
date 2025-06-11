from pydantic import BaseModel,field_validator
from pydantic import Field
from app.auth.schemas import UserOut



class ProductCreate(BaseModel):
    name: str = Field(..., description="The name of the product")
    description: str = Field(..., description="The full description of the product")
    price: float = Field(...,gt=0, description="The price of the product")
    stock: int = Field(...,ge=0, description="The stock quantity of the product")
    category: str = Field(..., description="The category of the product")
    image_url: str = Field(..., description="The image URL of the product")



    @field_validator('name','category','image_url')
    # @field_validator('category')
    # @field_validator('image_url')
    def name_not_empty(cls, v):
        if not v.strip():
            raise ValueError(f'{v} cannot be empty or whitespace.')
        return v





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