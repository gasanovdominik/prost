from pydantic import BaseModel, EmailStr
from datetime import datetime, date
from enum import Enum
from typing import Optional


# --- Пользователь ---

class UserCreate(BaseModel):
    name: str
    email: EmailStr
    password: str

class UserOut(BaseModel):
    id: int
    name: str
    email: EmailStr
    role: str

    class Config:
        from_attributes = True  # Pydantic v2


class UserLogin(BaseModel):
    email: EmailStr
    password: str


# --- Токены ---

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    email: Optional[str] = None


# --- Объявления (Listing) ---

class ListingBase(BaseModel):
    title: str
    description: str
    city: str
    district: str
    price: float
    housing_type: str  # квартира, дом и т.д.
    rooms: int

class ListingCreate(ListingBase):
    pass

class ListingUpdate(ListingBase):
    status: Optional[bool] = True

class ListingOut(ListingBase):
    id: int
    status: bool
    created_at: datetime
    owner_id: int

    class Config:
        from_attributes = True  # Pydantic v2


class BookingBase(BaseModel):
    listing_id: int
    start_date: date
    end_date: date

class BookingCreate(BookingBase):
    pass

class BookingOut(BaseModel):
    id: int
    listing_id: int
    start_date: date
    end_date: date
    status: str
    user_id: int

    class Config:
        from_attributes = True


class ReviewCreate(BaseModel):
    listing_id: int
    rating: int  # 1–5
    comment: str

class ReviewOut(BaseModel):
    id: int
    listing_id: int
    user_id: int
    rating: int
    comment: str
    created_at: datetime

    class Config:
        from_attributes = True


class PopularSearchOut(BaseModel):
    keyword: str
    count: int

class ViewedListingOut(BaseModel):
    id: int
    title: str
    viewed_at: datetime

    class Config:
        from_attributes = True

class FavoriteOut(BaseModel):
    id: int
    listing_id: int

    class Config:
        from_attributes = True
class SupportCreate(BaseModel):
    subject: str
    message: str

class SupportOut(BaseModel):
    id: int
    user_id: int
    subject: str
    message: str
    created_at: datetime

    class Config:
        from_attributes = True

class WalletOut(BaseModel):
    balance: float

    class Config:
        from_attributes = True

class TopUpRequest(BaseModel):
    amount: float

class TransactionOut(BaseModel):
    id: int
    amount: float
    description: str
    created_at: datetime

    class Config:
        from_attributes = True

