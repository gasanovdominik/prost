# ✅ routers/search.py
from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional
from back.database import get_db
from back.schemas import ListingOut, UserOut, PopularSearchOut
from back.crud.search import search_listings
from back.crud import searches as crud_searches
from back.auth import get_current_user

router = APIRouter()

@router.get("/", response_model=list[ListingOut])
async def search(
    query: Optional[str] = None,
    city: Optional[str] = None,
    district: Optional[str] = None,
    min_price: Optional[float] = None,
    max_price: Optional[float] = None,
    rooms_from: Optional[int] = None,
    rooms_to: Optional[int] = None,
    housing_type: Optional[str] = None,
    sort: Optional[str] = Query(None, description="price_asc, price_desc, date_new, date_old"),
    db: AsyncSession = Depends(get_db),
    current_user: UserOut = Depends(get_current_user)
):
    if query:
        await crud_searches.save_search(db, current_user.id, query)

    filters = {
        "query": query,
        "city": city,
        "district": district,
        "min_price": min_price,
        "max_price": max_price,
        "rooms_from": rooms_from,
        "rooms_to": rooms_to,
        "housing_type": housing_type,
        "sort": sort,
    }
    return await search_listings(db, filters)

@router.get("/popular", response_model=list[PopularSearchOut])
async def get_popular_searches(
    db: AsyncSession = Depends(get_db)
):
    results = await crud_searches.get_popular_searches(db)
    return [{"keyword": r[0], "count": r[1]} for r in results]

