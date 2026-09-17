from pydantic import BaseModel, EmailStr, ConfigDict, field_validator
from uuid import UUID
from datetime import datetime

class LoginRequest(BaseModel):
    email: EmailStr
    password: str

class UserCreate(BaseModel):
    email: EmailStr
    password: str

    @field_validator("password")
    @classmethod
    def password_must_be_at_least_8_chars(cls, v):
        if len(v) < 8:
            raise ValueError("Password must be at least 8 characters")
        return v

class UserResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    
    id: UUID
    email: EmailStr
    base_currency: str
    created_at: datetime