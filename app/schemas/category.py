from pydantic import BaseModel, ConfigDict
from uuid import UUID
from datetime import datetime


class CategoryBase(BaseModel):
    name: str
    is_expense: bool = True

class CategoryCreate(CategoryBase):
    pass

class CategoryResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    user_id: UUID
    name: str
    is_expense: bool
    created_at: datetime
