from pydantic import BaseModel, EmailStr, Field, field_validator

class UserCreate(BaseModel):
    email: EmailStr = Field(..., description="The email address of the user")
    password: str = Field(
        ...,
        min_length=8,
        # pattern=r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[!@#$%^&*()_+\-=\[\]{};':\"\\|,.<>\/?]).{8,}$",
        description="Password must be at least 8 characters long, with uppercase, lowercase, digit, and special character."
    )
    full_name: str = Field(..., description="The full name of the user")




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