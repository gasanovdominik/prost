from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from back.auth import get_current_user
from back.database import get_db
from back.schemas import WalletOut, TopUpRequest, TransactionOut, UserOut
from back.crud import wallet as crud_wallet

router = APIRouter()

@router.get("/", response_model=WalletOut)
async def get_balance(
    db: AsyncSession = Depends(get_db),
    current_user: UserOut = Depends(get_current_user)
):
    return await crud_wallet.get_or_create_wallet(db, current_user.id)

@router.post("/topup", response_model=WalletOut)
async def top_up_balance(
    data: TopUpRequest,
    db: AsyncSession = Depends(get_db),
    current_user: UserOut = Depends(get_current_user)
):
    return await crud_wallet.top_up(db, current_user.id, data.amount)

@router.get("/transactions", response_model=list[TransactionOut])
async def get_my_transactions(
    db: AsyncSession = Depends(get_db),
    current_user: UserOut = Depends(get_current_user)
):
    return await crud_wallet.get_transactions(db, current_user.id)
