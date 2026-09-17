import uuid
from decimal import Decimal
from sqlalchemy import String, Numeric, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column
from app.models.base import AbstractBase

class Budget(AbstractBase):
    __tablename__ = "budgets"

    user_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    category_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("categories.id", ondelete="CASCADE"), nullable=False)
    limit_amount: Mapped[Decimal] = mapped_column(Numeric(10, 2), nullable=False)