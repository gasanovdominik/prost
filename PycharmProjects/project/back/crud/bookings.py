from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from back.models import Booking, BookingStatus
from back.schemas import BookingCreate

async def create_booking(db: AsyncSession, data: BookingCreate, user_id: int):
    booking = Booking(**data.dict(), user_id=user_id)
    db.add(booking)
    await db.commit()
    await db.refresh(booking)
    return booking

async def get_user_bookings(db: AsyncSession, user_id: int):
    result = await db.execute(select(Booking).where(Booking.user_id == user_id))
    return result.scalars().all()

async def cancel_booking(db: AsyncSession, booking_id: int, user_id: int):
    result = await db.execute(select(Booking).where(Booking.id == booking_id, Booking.user_id == user_id))
    booking = result.scalar_one_or_none()
    if booking and booking.status == BookingStatus.pending:
        booking.status = BookingStatus.cancelled
        await db.commit()
        await db.refresh(booking)
        return booking
    return None

async def update_booking_status(db: AsyncSession, booking_id: int, status: BookingStatus):
    result = await db.execute(select(Booking).where(Booking.id == booking_id))
    booking = result.scalar_one_or_none()
    if booking:
        booking.status = status
        await db.commit()
        await db.refresh(booking)
        return booking
    return None
