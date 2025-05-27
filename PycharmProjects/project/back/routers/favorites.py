from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from back.database import get_db
from back.auth import get_current_user
from back.schemas import UserOut, FavoriteOut
from back.crud import favorites as crud_favorites

router = APIRouter()

@router.post("/{listing_id}", response_model=FavoriteOut)
async def add_favorite(
    listing_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: UserOut = Depends(get_current_user)
):
    return await crud_favorites.add_favorite(db, current_user.id, listing_id)

@router.delete("/{listing_id}")
async def delete_favorite(
    listing_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: UserOut = Depends(get_current_user)
):
    deleted = await crud_favorites.remove_favorite(db, current_user.id, listing_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Избранное не найдено")
    return {"message": "Удалено"}

@router.get("/", response_model=list[FavoriteOut])
async def list_favorites(
    db: AsyncSession = Depends(get_db),
    current_user: UserOut = Depends(get_current_user)
):
    return await crud_favorites.get_favorites(db, current_user.id)
