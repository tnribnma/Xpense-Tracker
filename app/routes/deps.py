from fastapi import Depends,HTTPException,status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID
from app.core.database import get_db
from app.models.user import User
from app.core.security import decode_token
from app.repositories.user_repository import UserRepository

oauth2_scheme=OAuth2PasswordBearer(tokenUrl="auth/login")

async def get_current_user(
    token:str=Depends(oauth2_scheme)
    ,db:AsyncSession=Depends(get_db)
)->User:
    user_id=decode_token(token)

    if not user_id:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="Unauthorized",headers={"WWW-Authenticate": "Bearer"})

    try:
        _user_=UUID(user_id)
    except (ValueError, TypeError):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="Unauthorized",headers={"WWW-Authenticate": "Bearer"})

    repo=UserRepository(db)
    user=await repo.get_by_id(_user_)

    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="Unauthorized",headers={"WWW-Authenticate": "Bearer"})

    return user