from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from back.models import Favorite

async def add_favorite(db: AsyncSession, user_id: int, listing_id: int):
    favorite = Favorite(user_id=user_id, listing_id=listing_id)
    db.add(favorite)
    await db.commit()
    await db.refresh(favorite)
    return favorite

async def remove_favorite(db: AsyncSession, user_id: int, listing_id: int):
    result = await db.execute(
        select(Favorite).where(Favorite.user_id == user_id, Favorite.listing_id == listing_id)
    )
    favorite = result.scalar_one_or_none()
    if favorite:
        await db.delete(favorite)
        await db.commit()
        return True
    return False

async def get_favorites(db: AsyncSession, user_id: int):
    result = await db.execute(
        select(Favorite).where(Favorite.user_id == user_id)
    )
    return result.scalars().all()
