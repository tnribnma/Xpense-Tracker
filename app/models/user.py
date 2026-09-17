from sqlalchemy import String
from sqlalchemy.orm import Mapped,mapped_column
from app.models.base import AbstractBase

class User(AbstractBase):
    __tablename__="users"

    email:Mapped[str]=mapped_column(
        String(255),
        unique=True,
        index=True,
        nullable=False
    )
    hashed_password:Mapped[str]=mapped_column(
        String(255),
        nullable=False
    )
    base_currency:Mapped[str]=mapped_column(
        String(3),
        default="USD",
        nullable=False
    )