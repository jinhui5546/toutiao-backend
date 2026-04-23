from sqlalchemy import select, func, delete
from sqlalchemy.ext.asyncio import AsyncSession

from models.favorite import Favorite
from models.news import NewList


async def check_favorite(db: AsyncSession, user_id: int, news_id: int) -> bool:
    """检查用户是否已收藏某新闻"""
    stmt = select(Favorite).where(
        Favorite.user_id == user_id,
        Favorite.news_id == news_id
    )
    result = await db.execute(stmt)
    return result.scalar_one_or_none() is not None


async def add_favorite(db: AsyncSession, user_id: int, news_id: int) -> Favorite:
    """添加收藏"""
    favorite = Favorite(user_id=user_id, news_id=news_id)
    db.add(favorite)
    await db.commit()
    await db.refresh(favorite)
    return favorite


async def remove_favorite(db: AsyncSession, user_id: int, news_id: int):
    """取消收藏"""
    stmt = delete(Favorite).where(
        Favorite.user_id == user_id,
        Favorite.news_id == news_id
    )
    result = await db.execute(stmt)
    await db.commit()
    return result.rowcount > 0


async def get_favorite_list(db: AsyncSession, user_id: int, page: int = 1, page_size: int = 10):
    """获取用户收藏列表"""
    offset = (page - 1) * page_size
    
    # 查询收藏记录并关联新闻信息
    stmt = (
        select(Favorite, NewList)
        .join(NewList, Favorite.news_id == NewList.id)
        .where(Favorite.user_id == user_id)
        .order_by(Favorite.created_at.desc())
        .offset(offset)
        .limit(page_size)
    )
    result = await db.execute(stmt)
    favorites = result.all()
    
    # 获取总数
    count_stmt = select(func.count(Favorite.id)).where(Favorite.user_id == user_id)
    count_result = await db.execute(count_stmt)
    total = count_result.scalar_one()
    
    return favorites, total


async def clear_all_favorites(db: AsyncSession, user_id: int):
    """清空用户所有收藏"""
    stmt = delete(Favorite).where(Favorite.user_id == user_id)
    result = await db.execute(stmt)
    await db.commit()
    return result.rowcount
