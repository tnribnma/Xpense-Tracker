from pydantic import BaseModel, ConfigDict
from uuid import UUID
from datetime import datetime
from decimal import Decimal


class TransactionBase(BaseModel):
    original_amount: Decimal
    original_currency: str
    category_id: UUID
    description: str | None = None
    date: datetime

class TransactionCreate(TransactionBase):
    pass

class TransactionResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    user_id: UUID
    original_amount: Decimal
    original_currency: str
    exchange_rate: Decimal
    base_amount: Decimal
    category_id: UUID | None = None
    description: str | None = None
    date: datetime
    receipt_url: str | None = None
    created_at: datetime
