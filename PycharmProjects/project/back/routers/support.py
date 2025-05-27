from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from back.auth import get_current_user
from back.database import get_db
from back.schemas import SupportCreate, SupportOut, UserOut
from back.crud import support as crud_support

router = APIRouter()

@router.post("/", response_model=SupportOut)
async def send_support_message(
    data: SupportCreate,
    db: AsyncSession = Depends(get_db),
    current_user: UserOut = Depends(get_current_user)
):
    return await crud_support.create_message(db, current_user.id, data.subject, data.message)

@router.get("/my", response_model=list[SupportOut])
async def get_my_messages(
    db: AsyncSession = Depends(get_db),
    current_user: UserOut = Depends(get_current_user)
):
    return await crud_support.get_user_messages(db, current_user.id)

@router.get("/all", response_model=list[SupportOut])
async def get_all_support_messages(
    db: AsyncSession = Depends(get_db),
    current_user: UserOut = Depends(get_current_user)
):
    if current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Доступ запрещён")
    return await crud_support.get_all_messages(db)
