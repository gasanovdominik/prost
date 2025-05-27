from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import func, select
from back.models import View, Listing

async def record_view(db: AsyncSession, user_id: int, listing_id: int):
    view = View(user_id=user_id, listing_id=listing_id)
    db.add(view)
    await db.commit()

async def get_most_viewed(db: AsyncSession, limit: int = 10):
    result = await db.execute(
        select(Listing, func.count(View.id).label("views"))
        .join(View, View.listing_id == Listing.id)
        .group_by(Listing.id)
        .order_by(func.count(View.id).desc())
        .limit(limit)
    )
    return result.all()
