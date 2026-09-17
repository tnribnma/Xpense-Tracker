from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_db
from app.routes.deps import get_current_user
from app.models.user import User
from app.schemas.category import CategoryCreate, CategoryResponse
from app.repositories.category_repository import CategoryRepository

router = APIRouter(prefix="/categories", tags=["Categories"])

@router.post("/", response_model=CategoryResponse, status_code=status.HTTP_201_CREATED)
async def create_category(
    category: CategoryCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    repo = CategoryRepository(db)
    new_category = await repo.create_category(category, current_user.id)
    return new_category

@router.get("/", response_model=list[CategoryResponse])
async def read_categories(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    repo = CategoryRepository(db)
    categories = await repo.get_user_categories(current_user.id)
    return categories