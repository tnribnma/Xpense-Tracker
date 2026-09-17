from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.category import Category
from app.schemas.category import CategoryCreate
from uuid import UUID
from typing import Sequence

class CategoryRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_category_by_id(self, category_id: UUID, user_id: UUID) -> Category | None:
        result = await self.db.execute(
            select(Category).where(Category.id == category_id, Category.user_id == user_id)
        )
        return result.scalar_one_or_none()

    async def get_user_categories(self, user_id: UUID) -> Sequence[Category]:
        result = await self.db.execute(
            select(Category).where(Category.user_id == user_id)
        )
        return result.scalars().all()

    async def create_category(self, category_data: CategoryCreate, user_id: UUID) -> Category:
        new_category = Category(**category_data.model_dump(), user_id=user_id)
        self.db.add(new_category)
        await self.db.commit()
        await self.db.refresh(new_category)
        return new_category