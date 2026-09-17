from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func,extract
from app.models.transaction import Transaction
from app.schemas.transaction import TransactionCreate
from uuid import UUID
from typing import Any, Sequence
from app.models.category import Category

class TransactionRepository:
    def __init__(self,db:AsyncSession):
        self.db=db

    async def create(self,transaction_data:dict)->Transaction:
        new_transaction=Transaction(**transaction_data)
        self.db.add(new_transaction)
        await self.db.commit()
        await self.db.refresh(new_transaction)
        return new_transaction

    async def get_user_transactions(self,user_id:UUID,skip:int=0,limit:int=50)->Sequence[Transaction]:
        result=await self.db.execute(
            select(Transaction)
            .where(Transaction.user_id==user_id)
            .order_by(Transaction.date.desc())
            .offset(skip)
            .limit(limit)
        )
        return result.scalars().all()

    async def get_monthly_summary(self, user_id: UUID, year: int, month: int) -> Sequence[Any]:
        result = await self.db.execute(
            select(
                Category.id.label("category_id"),
                Category.name.label("category_name"),
                func.sum(Transaction.base_amount).label("total_spent"),
                func.count(Transaction.id).label("transaction_count")
            )
            .join(Transaction, Transaction.category_id == Category.id)
            .where(
                Transaction.user_id == user_id,
                extract('year', Transaction.date) == year,
                extract('month', Transaction.date) == month
            )
            .group_by(Category.id, Category.name)
            .order_by(func.sum(Transaction.base_amount).desc())
        )
        return result.all()
