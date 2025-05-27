from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from back.auth import get_current_user
from back.database import get_db
from back.schemas import BookingCreate, BookingOut, UserOut
from back.crud import bookings as crud_bookings
from back.models import BookingStatus
print("✅ bookings.py загружен")

router = APIRouter()

@router.post("/", response_model=BookingOut)
async def create_booking(
    booking: BookingCreate,
    db: AsyncSession = Depends(get_db),
    current_user: UserOut = Depends(get_current_user)
):
    return await crud_bookings.create_booking(db, booking, current_user.id)

@router.get("/my", response_model=list[BookingOut])
async def get_my_bookings(
    db: AsyncSession = Depends(get_db),
    current_user: UserOut = Depends(get_current_user)
):
    return await crud_bookings.get_user_bookings(db, current_user.id)

@router.post("/{booking_id}/cancel", response_model=BookingOut)
async def cancel(
    booking_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: UserOut = Depends(get_current_user)
):
    result = await crud_bookings.cancel_booking(db, booking_id, current_user.id)
    if not result:
        raise HTTPException(status_code=400, detail="Невозможно отменить бронирование")
    return result

@router.post("/{booking_id}/confirm", response_model=BookingOut)
async def confirm(
    booking_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: UserOut = Depends(get_current_user)
):
    return await crud_bookings.update_booking_status(db, booking_id, BookingStatus.confirmed)

@router.post("/{booking_id}/reject", response_model=BookingOut)
async def reject(
    booking_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: UserOut = Depends(get_current_user)
):
    return await crud_bookings.update_booking_status(db, booking_id, BookingStatus.rejected)
