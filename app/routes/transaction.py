from fastapi import status,Depends,APIRouter,Query
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi.responses import StreamingResponse
from app.schemas.transaction import TransactionResponse,TransactionCreate
from app.core.database import get_db
from app.models.user import User
from app.services.transaction_service import TransactionService
from app.routes.deps import get_current_user
import io
from app.schemas.analytics import CategoryBreakdown


router =APIRouter(prefix="/transactions",tags=["Transactions"])

@router.post("/",response_model=TransactionResponse,status_code=status.HTTP_201_CREATED)
async def create_transaction(
    transaction:TransactionCreate,
    db:AsyncSession=Depends(get_db),
    current_user:User=Depends(get_current_user)
):
    service=TransactionService(db)
    new_transaction=await service.create_transaction(transaction,current_user)
    return new_transaction

@router.get("/",response_model=list[TransactionResponse])
async def read_transaction(
    skip:int=Query(0,ge=0),
    limit:int=Query(50,ge=1,le=100),
    db:AsyncSession=Depends(get_db),
    current_user:User=Depends(get_current_user)
):
    service=TransactionService(db)
    transactions=await service.get_user_transactions(current_user, skip, limit)
    return transactions

@router.get("/analytics/monthly-breakdown", response_model=list[CategoryBreakdown])
async def get_monthly_breakdown(
    year: int = Query(..., ge=2000, le=2100),
    month: int = Query(..., ge=1, le=12),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    service = TransactionService(db)
    breakdown = await service.get_monthly_breakdown(current_user, year, month)
    return breakdown

@router.get("/export/csv")
async def export_transactions_csv(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    service = TransactionService(db)
    csv_data = await service.export_user_transactions_csv(current_user)
    
    response = StreamingResponse(io.StringIO(csv_data), media_type="text/csv")
    response.headers["Content-Disposition"] = "attachment; filename=transactions.csv"
    return response
