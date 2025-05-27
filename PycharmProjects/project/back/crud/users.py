from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from back.models import User
from back.auth import get_password_hash, verify_password

async def get_user_by_email(db: AsyncSession, email: str):
    result = await db.execute(select(User).where(User.email == email))
    return result.scalars().first()

async def create_user(db: AsyncSession, user_data):
    hashed_pw = get_password_hash(user_data.password)
    user = User(
        name=user_data.name,
        email=user_data.email,
        hashed_password=hashed_pw,
        role="tenant"
    )
    db.add(user)
    await db.commit()
    await db.refresh(user)
    return user

async def authenticate_user(db: AsyncSession, email: str, password: str):
    user = await get_user_by_email(db, email)
    if user and verify_password(password, user.hashed_password):
        return user
    return None
