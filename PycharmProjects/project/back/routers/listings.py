from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from back.auth import get_current_user
from back.database import get_db
from back.schemas import ListingCreate, ListingOut, ListingUpdate, UserOut
from back.crud import views as crud_views, listings as crud_listings

router = APIRouter()

@router.post("/", response_model=ListingOut)
async def create_listing(
    listing: ListingCreate,
    db: AsyncSession = Depends(get_db),
    current_user: UserOut = Depends(get_current_user),
):
    return await crud_listings.create_listing(db, listing, current_user.id)

@router.get("/my", response_model=list[ListingOut])
async def get_my_listings(
    db: AsyncSession = Depends(get_db),
    current_user: UserOut = Depends(get_current_user),
):
    return await crud_listings.get_user_listings(db, current_user.id)

@router.get("/{listing_id}", response_model=ListingOut)
async def get_listing(
        listing_id: int,
        db: AsyncSession = Depends(get_db),
        current_user: UserOut = Depends(get_current_user)
):
    listing = await crud_listings.get_listing(db, listing_id)
    if not listing:
        raise HTTPException(status_code=404, detail="Объявление не найдено")

    await crud_views.record_view(db, current_user.id, listing_id)  # ← добавили запись
    return listing


@router.put("/{listing_id}", response_model=ListingOut)
async def update_listing(
    listing_id: int,
    data: ListingUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: UserOut = Depends(get_current_user),
):
    listing = await crud_listings.update_listing(db, listing_id, data, current_user.id)
    if not listing:
        raise HTTPException(status_code=404, detail="Объявление не найдено или доступ запрещен")
    return listing

@router.delete("/{listing_id}", response_model=ListingOut)
async def delete_listing(
    listing_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: UserOut = Depends(get_current_user),
):
    listing = await crud_listings.delete_listing(db, listing_id, current_user.id)
    if not listing:
        raise HTTPException(status_code=404, detail="Объявление не найдено или доступ запрещен")
    return listing

@router.patch("/{listing_id}/toggle-status", response_model=ListingOut)
async def toggle_status(
    listing_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: UserOut = Depends(get_current_user),
):
    listing = await crud_listings.toggle_listing_status(db, listing_id, current_user.id)
    if not listing:
        raise HTTPException(status_code=404, detail="Объявление не найдено или доступ запрещен")
    return listing

@router.get("/popular", response_model=list[ListingOut])
async def popular_listings(
    db: AsyncSession = Depends(get_db)
):
    results = await crud_views.get_most_viewed(db)
    listings = [listing for listing, _ in results]
    return listings
