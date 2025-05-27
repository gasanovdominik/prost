from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import or_, desc, asc
from back.models import Listing

async def search_listings(db: AsyncSession, filters: dict):
    query = select(Listing).where(Listing.status == True)

    if keyword := filters.get("query"):
        query = query.where(
            or_(
                Listing.title.ilike(f"%{keyword}%"),
                Listing.description.ilike(f"%{keyword}%")
            )
        )
    if city := filters.get("city"):
        query = query.where(Listing.city.ilike(f"%{city}%"))
    if district := filters.get("district"):
        query = query.where(Listing.district.ilike(f"%{district}%"))
    if min_price := filters.get("min_price"):
        query = query.where(Listing.price >= min_price)
    if max_price := filters.get("max_price"):
        query = query.where(Listing.price <= max_price)
    if rooms_from := filters.get("rooms_from"):
        query = query.where(Listing.rooms >= rooms_from)
    if rooms_to := filters.get("rooms_to"):
        query = query.where(Listing.rooms <= rooms_to)
    if housing_type := filters.get("housing_type"):
        query = query.where(Listing.housing_type.ilike(f"%{housing_type}%"))

    sort = filters.get("sort")
    if sort == "price_asc":
        query = query.order_by(asc(Listing.price))
    elif sort == "price_desc":
        query = query.order_by(desc(Listing.price))
    elif sort == "date_new":
        query = query.order_by(desc(Listing.created_at))
    elif sort == "date_old":
        query = query.order_by(asc(Listing.created_at))

    result = await db.execute(query)
    return result.scalars().all()
