from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from back.schemas import ReviewCreate, ReviewOut, UserOut
from back.auth import get_current_user
from back.database import get_db
from back.crud import reviews as crud_reviews
from back.models import Booking, BookingStatus
from sqlalchemy.future import select
router = APIRouter()

@router.get("/{listing_id}", response_model=list[ReviewOut])
async def get_reviews(
    listing_id: int,
    db: AsyncSession = Depends(get_db)
):
    return await crud_reviews.get_reviews_by_listing(db, listing_id)

@router.post("/", response_model=ReviewOut)
async def add_review(
    review: ReviewCreate,
    db: AsyncSession = Depends(get_db),
    current_user: UserOut = Depends(get_current_user)
):
    # Проверка: есть ли подтверждённая бронь на этот объект
    result = await db.execute(
        select(Booking).where(
            Booking.listing_id == review.listing_id,
            Booking.user_id == current_user.id,
            Booking.status == BookingStatus.confirmed
        )
    )
    booking = result.scalar_one_or_none()
    if not booking:
        raise HTTPException(
            status_code=403,
            detail="Вы можете оставить отзыв только после подтверждённой брони."
        )

    return await crud_reviews.create_review(db, review, current_user.id)
