from pydantic import BaseModel
from decimal import Decimal
from uuid import UUID

class CategoryBreakdown(BaseModel):
    category_id: UUID
    category_name: str
    total_spent: Decimal
    transaction_count: int