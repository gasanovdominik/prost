from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from back.models import Listing
from back.schemas import ListingCreate, ListingUpdate

async def create_listing(db: AsyncSession, data: ListingCreate, user_id: int):
    listing = Listing(**data.dict(), owner_id=user_id)
    db.add(listing)
    await db.commit()
    await db.refresh(listing)
    return listing

async def get_user_listings(db: AsyncSession, user_id: int):
    result = await db.execute(select(Listing).where(Listing.owner_id == user_id))
    return result.scalars().all()

async def get_listing_by_id(db: AsyncSession, listing_id: int):
    result = await db.execute(select(Listing).where(Listing.id == listing_id))
    return result.scalar_one_or_none()

async def update_listing(db: AsyncSession, listing_id: int, data: ListingUpdate, user_id: int):
    result = await db.execute(select(Listing).where(Listing.id == listing_id, Listing.owner_id == user_id))
    listing = result.scalar_one_or_none()
    if not listing:
        return None
    for key, value in data.dict(exclude_unset=True).items():
        setattr(listing, key, value)
    await db.commit()
    await db.refresh(listing)
    return listing

async def delete_listing(db: AsyncSession, listing_id: int, user_id: int):
    listing = await get_listing_by_id(db, listing_id)
    if listing and listing.owner_id == user_id:
        await db.delete(listing)
        await db.commit()
        return listing
    return None

async def toggle_listing_status(db: AsyncSession, listing_id: int, user_id: int):
    listing = await get_listing_by_id(db, listing_id)
    if listing and listing.owner_id == user_id:
        listing.status = not listing.status
        await db.commit()
        await db.refresh(listing)
        return listing
    return None

