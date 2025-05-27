from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from back.models import Wallet, Transaction


async def get_or_create_wallet(db: AsyncSession, user_id: int):
    result = await db.execute(select(Wallet).where(Wallet.user_id == user_id))
    wallet = result.scalar_one_or_none()
    if not wallet:
        wallet = Wallet(user_id=user_id, balance=0.0)
        db.add(wallet)
        await db.commit()
        await db.refresh(wallet)
    return wallet

async def top_up(db: AsyncSession, user_id: int, amount: float):
    wallet = await get_or_create_wallet(db, user_id)
    wallet.balance += amount
    transaction = Transaction(user_id=user_id, amount=amount, description="Пополнение баланса")
    db.add(transaction)
    await db.commit()
    await db.refresh(wallet)
    return wallet

async def get_transactions(db: AsyncSession, user_id: int):
    result = await db.execute(select(Transaction).where(Transaction.user_id == user_id))
    return result.scalars().all()
