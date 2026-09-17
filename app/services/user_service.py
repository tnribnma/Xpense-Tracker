from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException,status
from app.repositories.user_repository import UserRepository
from app.schemas.user import UserCreate
from app.core.security import get_hash_password,verify_password,create_access_token
from app.models.user import User


class UserService:
    def __init__(self,db:AsyncSession):
        self.db=db
        self.user_repo=UserRepository(db)

    async def register_user(self,user_create:UserCreate)->User:
        existing_user=await self.user_repo.get_by_email(user_create.email)

        if existing_user:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail="email exist")
        try:
            hashed_password=get_hash_password(user_create.password)
        except ValueError:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail="Password cannot be longer than 72 bytes",
            )
        new_user=await self.user_repo.create(user_create,hashed_password)

        return new_user

    async def authenticate_user(self,email:str,password:str)->str:
        user=await self.user_repo.get_by_email(email)
        invalid=HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="incorrect email or password")

        if not user or not verify_password(password,user.hashed_password):
            raise invalid

        return create_access_token(subject=str(user.id))
