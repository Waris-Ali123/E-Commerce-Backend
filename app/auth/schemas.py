from pydantic import BaseModel, EmailStr, Field, field_validator, ConfigDict
from .models import UserRole

class UserCreate(BaseModel):
    email: EmailStr = Field(..., description="The email address of the user")
    password: str = Field(
        ...,
        min_length=8,
        description="Password must be at least 8 characters long, with uppercase, lowercase, digit, and special character."
    )
    full_name: str = Field(..., description="The full name of the user")
    role: str = Field(default=UserRole.USER.value,pattern="^(USER|ADMIN)$", description="The role of the user, default is 'user'")


    @field_validator('full_name')
    def name_not_empty(cls, v):
        if not v.strip():
            raise ValueError('Full name cannot be empty or whitespace.')
        return v



    @field_validator('password')
    def password_complexity(cls, v):
        import re

        if (len(v) < 8 or
            not re.search(r'[A-Z]', v) or
            not re.search(r'[a-z]', v) or
            not re.search(r'\d', v) or
            not re.search(r'[!@#$%^&*()_+\-=\[\]{};\'":\\|,.<>\/?]', v)):
            raise ValueError('Password must be at least 8 characters long, with uppercase, lowercase, digit, and special character.')
    
        return v
    


class UserOut(BaseModel):
    id: int
    email: EmailStr
    name: str
    role: UserRole
    model_config = ConfigDict(from_attributes=True)

    # class Config:
    #     orm_mode = True 
    #     from_attributes = True #for pydantic v2 compatibility






class PasswordReset(BaseModel):
    token : str
    new_password: str

    @field_validator('new_password')
    def password_complexity(cls, v):
        import re
        if (len(v) < 8 or
            not re.search(r'[A-Z]', v) or
            not re.search(r'[a-z]', v) or
            not re.search(r'\d', v) or
            not re.search(r'[!@#$%^&*()_+\-=\[\]{};\'":\\|,.<>\/?]', v)):
            raise ValueError('Password must be at least 8 characters long, with uppercase, lowercase, digit, and special character.')
        return v
    
    @field_validator('token')
    def token_not_empty(cls, v):
        if not v.strip():
            raise ValueError('token cannot be empty or whitespace.')
        return v