from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from back.models import Review
from back.schemas import ReviewCreate

async def create_review(db: AsyncSession, data: ReviewCreate, user_id: int):
    review = Review(**data.dict(), user_id=user_id)
    db.add(review)
    await db.commit()
    await db.refresh(review)
    return review

async def get_reviews_by_listing(db: AsyncSession, listing_id: int):
    result = await db.execute(
        select(Review).where(Review.listing_id == listing_id)
    )
    return result.scalars().all()
