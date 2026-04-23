from sqlalchemy import select, func, delete
from sqlalchemy.ext.asyncio import AsyncSession

from models.history import History
from models.news import NewList


async def add_history(db: AsyncSession, user_id: int, news_id: int) -> History:
    """添加浏览历史记录"""
    # 检查是否已存在该记录，如果存在则更新
    stmt = select(History).where(
        History.user_id == user_id,
        History.news_id == news_id
    )
    result = await db.execute(stmt)
    existing = result.scalar_one_or_none()
    
    if existing:
        # 如果存在，更新时间已在模型中通过 default 处理，这里直接返回
        await db.refresh(existing)
        return existing
    
    # 创建新记录
    history = History(user_id=user_id, news_id=news_id)
    db.add(history)
    await db.commit()
    await db.refresh(history)
    return history


async def get_history_list(db: AsyncSession, user_id: int, page: int = 1, page_size: int = 10):
    """获取用户浏览历史列表"""
    offset = (page - 1) * page_size
    
    # 查询历史记录并关联新闻信息
    stmt = (
        select(History, NewList)
        .join(NewList, History.news_id == NewList.id)
        .where(History.user_id == user_id)
        .order_by(History.created_at.desc())
        .offset(offset)
        .limit(page_size)
    )
    result = await db.execute(stmt)
    histories = result.all()
    
    # 获取总数
    count_stmt = select(func.count(History.id)).where(History.user_id == user_id)
    count_result = await db.execute(count_stmt)
    total = count_result.scalar_one()
    
    return histories, total


async def delete_history(db: AsyncSession, history_id: int, user_id: int) -> bool:
    """删除单条浏览历史记录"""
    stmt = delete(History).where(
        History.id == history_id,
        History.user_id == user_id
    )
    result = await db.execute(stmt)
    await db.commit()
    return result.rowcount > 0


async def clear_all_history(db: AsyncSession, user_id: int):
    """清空用户所有浏览历史"""
    stmt = delete(History).where(History.user_id == user_id)
    result = await db.execute(stmt)
    await db.commit()
    return result.rowcount
