from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID
from app.models.user import User
from app.schemas.user import UserCreate

class UserRepository:
    def __init__(self,db:AsyncSession):
        self.db=db

    async def get_by_email(self,email:str)->User|None:
        result=await self.db.execute(select(User).where(User.email==email))
        return result.scalar_one_or_none()
    
    async def get_by_id(self,id:UUID)->User|None:
        result=await self.db.execute(select(User).where(User.id==id))
        return result.scalar_one_or_none()

    async def create(self,user_create:UserCreate,hashed_password:str)->User:
        new_user=User(
        email=user_create.email,
        hashed_password=hashed_password
        )

        self.db.add(new_user)
        await self.db.commit()
        await self.db.refresh(new_user)
        return new_user       

