from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Boolean, Date, Enum
from sqlalchemy.orm import relationship
from back.database import Base
from datetime import datetime
import enum

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String, nullable=False)
    role = Column(String, default="tenant")  # 'tenant' или 'landlord'
    created_at = Column(DateTime, default=datetime.utcnow)

    listings = relationship("Listing", back_populates="owner")

class Listing(Base):
    __tablename__ = "listings"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    description = Column(String)
    city = Column(String)
    district = Column(String)
    price = Column(Float)
    housing_type = Column(String)  # квартира, дом и т.д.
    rooms = Column(Integer)
    status = Column(Boolean, default=True)  # активно/неактивно
    created_at = Column(DateTime, default=datetime.utcnow)

    owner_id = Column(Integer, ForeignKey("users.id"))
    owner = relationship("User", back_populates="listings")

class BookingStatus(str, enum.Enum):
    pending = "pending"
    confirmed = "confirmed"
    rejected = "rejected"
    cancelled = "cancelled"

class Booking(Base):
    __tablename__ = "bookings"

    id = Column(Integer, primary_key=True)
    listing_id = Column(Integer, ForeignKey("listings.id"))
    user_id = Column(Integer, ForeignKey("users.id"))
    start_date = Column(Date)
    end_date = Column(Date)
    status = Column(Enum(BookingStatus), default=BookingStatus.pending)

    listing = relationship("Listing")
    user = relationship("User")

class Review(Base):
    __tablename__ = "reviews"

    id = Column(Integer, primary_key=True)
    listing_id = Column(Integer, ForeignKey("listings.id"))
    user_id = Column(Integer, ForeignKey("users.id"))
    rating = Column(Integer)  # от 1 до 5
    comment = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)

    listing = relationship("Listing")
    user = relationship("User")

class View(Base):
    __tablename__ = "views"

    id = Column(Integer, primary_key=True)
    listing_id = Column(Integer, ForeignKey("listings.id"))
    user_id = Column(Integer, ForeignKey("users.id"))
    viewed_at = Column(DateTime, default=datetime.utcnow)

    listing = relationship("Listing")
    user = relationship("User")

class SearchQuery(Base):
    __tablename__ = "search_queries"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    keyword = Column(String)
    searched_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User")

class Favorite(Base):
    __tablename__ = "favorites"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    listing_id = Column(Integer, ForeignKey("listings.id"))

    user = relationship("User")
    listing = relationship("Listing")

class SupportMessage(Base):
    __tablename__ = "support_messages"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    subject = Column(String, nullable=False)
    message = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User")

class Wallet(Base):
    __tablename__ = "wallets"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), unique=True)
    balance = Column(Float, default=0.0)

    user = relationship("User")

class Transaction(Base):
    __tablename__ = "transactions"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    amount = Column(Float)
    description = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User")




