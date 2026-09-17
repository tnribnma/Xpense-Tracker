from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, extract
from app.models.budget import Budget
from app.models.transaction import Transaction
from datetime import datetime
from uuid import UUID
from typing import Sequence

class BudgetRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_budget_for_category(self, user_id: UUID, category_id: UUID) -> Budget | None:
        result = await self.db.execute(
            select(Budget).where(
                Budget.user_id == user_id,
                Budget.category_id == category_id
            )
        )
        return result.scalar_one_or_none()

    async def get_monthly_spent(self, user_id: UUID, category_id: UUID) -> float:
        current_year = datetime.now().year
        current_month = datetime.now().month
        
        result = await self.db.execute(
            select(func.sum(Transaction.base_amount)).where(
                Transaction.user_id == user_id,
                Transaction.category_id == category_id,
                extract('year', Transaction.date) == current_year,
                extract('month', Transaction.date) == current_month
            )
        )
        spent = result.scalar_one_or_none()
        return float(spent) if spent else 0.0
    