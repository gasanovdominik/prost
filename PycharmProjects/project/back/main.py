from fastapi import FastAPI
from back.database import Base, engine
from back.routers import listings, bookings, support, wallet
from back.routers import search, favorites, reviews, users

print("📦 bookings импортирован")

app = FastAPI()

# Подключаем роутеры
app.include_router(users.router, prefix="/users", tags=["Users"])
app.include_router(listings.router, prefix="/listings", tags=["Listings"])
app.include_router(search.router, prefix="/search", tags=["Search"])
app.include_router(bookings.router, prefix="/bookings", tags=["Bookings"])
app.include_router(reviews.router, prefix="/reviews", tags=["Reviews"])
app.include_router(favorites.router, prefix="/favorites", tags=["Favorites"])
app.include_router(support.router, prefix="/support", tags=["Support"])
app.include_router(wallet.router, prefix="/wallet", tags=["Wallet"])

@app.on_event("startup")
async def startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)