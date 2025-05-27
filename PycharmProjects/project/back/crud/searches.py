from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from back.models import SearchQuery

async def save_search(db: AsyncSession, user_id: int, keyword: str):
    search = SearchQuery(user_id=user_id, keyword=keyword)
    db.add(search)
    await db.commit()

async def get_popular_searches(db: AsyncSession, limit: int = 10):
    result = await db.execute(
        select(SearchQuery.keyword, func.count().label("count"))
        .group_by(SearchQuery.keyword)
        .order_by(func.count().desc())
        .limit(limit)
    )
    return result.all()
