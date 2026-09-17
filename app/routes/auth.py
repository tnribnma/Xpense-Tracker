from typing import Annotated
from fastapi import APIRouter,Depends,status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas.user import UserResponse,UserCreate,LoginRequest
from app.core.database import get_db
from app.services.user_service import UserService
from app.routes.deps import get_current_user
from app.models.user import User

router=APIRouter(prefix="/auth",tags=["Authentication"])

@router.post("/register",response_model=UserResponse,status_code=status.HTTP_201_CREATED)
async def register(user:UserCreate,db:AsyncSession=Depends(get_db)):
    service=UserService(db)
    new_user=await service.register_user(user)

    return new_user

@router.post("/login")
async def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()],db:AsyncSession=Depends(get_db)):
    service=UserService(db)
    access_token=await service.authenticate_user(form_data.username,form_data.password)
    return {"access_token": access_token, "token_type": "bearer"}

@router.post("/login-json")
async def login_json(credentials:LoginRequest,db:AsyncSession=Depends(get_db)):
    service=UserService(db)
    access_token=await service.authenticate_user(credentials.email,credentials.password)
    return {"access_token": access_token, "token_type": "bearer"}

@router.get("/me",response_model=UserResponse)
async def users_me(current_user:User=Depends(get_current_user)):
    return current_user