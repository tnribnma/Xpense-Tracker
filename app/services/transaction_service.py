from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.repositories.transaction_repository import TransactionRepository
from app.repositories.category_repository import CategoryRepository
from app.repositories.budget_repository import BudgetRepository
from app.utils.currency_api import get_exchange_rate
from app.utils.csv_export import generate_transactions_csv
from app.schemas.transaction import TransactionCreate
from app.schemas.analytics import CategoryBreakdown
from app.models.user import User
from typing import Sequence
from uuid import UUID
from arq import create_pool
from arq.connections import RedisSettings
from app.core.config import settings

_arq_pool = None


async def _get_arq_pool():
    global _arq_pool
    if _arq_pool is None:
        _arq_pool = await create_pool(RedisSettings.from_dsn(settings.REDIS_URL))
    return _arq_pool

class TransactionService:
    def __init__(self, db: AsyncSession):
        self.db = db
        self.transaction_repo = TransactionRepository(db)
        self.category_repo = CategoryRepository(db)
        self.budget_repo = BudgetRepository(db)

    async def create_transaction(self, transaction_data: TransactionCreate, current_user: User) -> dict:
        category = await self.category_repo.get_category_by_id(transaction_data.category_id, current_user.id)
        if not category:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Category not found")

        try:
            exchange_rate = await get_exchange_rate(transaction_data.original_currency, current_user.base_currency)
        except Exception:
            raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail="Currency service unavailable")

        base_amount = round(transaction_data.original_amount * exchange_rate, 2)

        transaction_dict = transaction_data.model_dump()
        transaction_dict.update({
            "user_id": current_user.id,
            "exchange_rate": exchange_rate,
            "base_amount": base_amount
        })
        new_transaction = await self.transaction_repo.create(transaction_dict)

        budget = await self.budget_repo.get_budget_for_category(current_user.id, category.id)
        if budget:
            spent = await self.budget_repo.get_monthly_spent(current_user.id, category.id)
            if spent > float(budget.limit_amount):
                try:
                    redis = await _get_arq_pool()
                    await redis.enqueue_job(
                        "send_budget_alert_email",
                        user_email=current_user.email,
                        category_name=category.name,
                        spent=spent,
                        limit=float(budget.limit_amount)
                    )
                except Exception:
                    pass

        return new_transaction

    async def get_user_transactions(self, current_user: User, skip: int = 0, limit: int = 50) -> Sequence:
        return await self.transaction_repo.get_user_transactions(current_user.id, skip, limit)

    async def get_monthly_breakdown(self, current_user: User, year: int, month: int) -> list[CategoryBreakdown]:
        rows = await self.transaction_repo.get_monthly_summary(current_user.id, year, month)
        return [
            CategoryBreakdown(
                category_id=row.category_id,
                category_name=row.category_name,
                total_spent=row.total_spent,
                transaction_count=row.transaction_count,
            )
            for row in rows
        ]

    async def export_user_transactions_csv(self, current_user: User) -> str:
        transactions = await self.transaction_repo.get_user_transactions(current_user.id, skip=0, limit=10_000)
        return generate_transactions_csv(transactions)