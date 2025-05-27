from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from back.models import SupportMessage

async def create_message(db: AsyncSession, user_id: int, subject: str, message: str):
    msg = SupportMessage(user_id=user_id, subject=subject, message=message)
    db.add(msg)
    await db.commit()
    await db.refresh(msg)
    return msg

async def get_user_messages(db: AsyncSession, user_id: int):
    result = await db.execute(select(SupportMessage).where(SupportMessage.user_id == user_id))
    return result.scalars().all()

async def get_all_messages(db: AsyncSession):
    result = await db.execute(select(SupportMessage))
    return result.scalars().all()
