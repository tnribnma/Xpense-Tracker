import uuid
from sqlalchemy import String, ForeignKey, Boolean
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column
from app.models.base import AbstractBase


class Category(AbstractBase):
    __tablename__ = "categories"

    user_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
    )
    name: Mapped[str] = mapped_column(String(50), nullable=False)
    is_expense: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
