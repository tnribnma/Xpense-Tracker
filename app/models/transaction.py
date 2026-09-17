import uuid
from datetime import datetime
from decimal import Decimal
from sqlalchemy import String, Numeric, DateTime, ForeignKey, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column
from app.models.base import AbstractBase


class Transaction(AbstractBase):
    __tablename__ = "transactions"

    user_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
    )
    category_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("categories.id", ondelete="SET NULL"),
        nullable=True,
    )

    original_amount: Mapped[Decimal] = mapped_column(Numeric(10, 2), nullable=False)
    original_currency: Mapped[str] = mapped_column(String(3), nullable=False)
    exchange_rate: Mapped[Decimal] = mapped_column(
        Numeric(18, 6), default=Decimal("1.0"), nullable=False
    )
    base_amount: Mapped[Decimal] = mapped_column(Numeric(10, 2), nullable=False)

    description: Mapped[str] = mapped_column(String(255), nullable=True)
    date: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    receipt_url: Mapped[str] = mapped_column(String(255), nullable=True)
