from sqlalchemy import select, func, update, values
from sqlalchemy.ext.asyncio import AsyncSession

from models.news import Category, NewList


async def get_news(db:AsyncSession,skip:int=0,limit:int =10):
    stmt = select(Category).offset(skip).limit(limit)
    result =await  db.execute(stmt)
    return result.scalars().all()

async def get_newlist(db:AsyncSession,category:int,skip:int=0,limit:int=10):
    stmt = select(NewList).where(NewList.category_id==category).offset(skip).limit(limit)
    result = await db.execute(stmt)
    return result.scalars().all()

async def get_news_count(db:AsyncSession,category:int):
    stmt = select(func.count(NewList.id)).where(NewList.category_id==category)
    result = await db.execute(stmt)
    return result.scalar_one()

async  def get_dtail(db:AsyncSession,news_id:int):
    stmt = select(NewList).where(NewList.id==news_id)
    result = await db.execute(stmt)
    return result.scalar_one_or_none()

async def get_related_views(db:AsyncSession,id:int):
   stmt = update(NewList).where(NewList.id == id).values(views = NewList.views + 1)
   result = await db.execute(stmt)
   await db.commit()
   return result.rowcount > 0

async def related_news(db:AsyncSession,id:int,category_id:int,limit:int=5):
    stmt = select(NewList).where(
        NewList.category_id == category_id,
        NewList.id != id
    ).order_by(
        NewList.views.desc(),
        NewList.publish_time.desc()
      ).limit(limit)
    result = await db.execute(stmt)
    related_news1 = result.scalars().all()
    return [{
        "id": new_detail.id,
        "title": new_detail.title,
        "content": new_detail.content,
        "image": new_detail.image,
        "author": new_detail.author,
        "publishTime": new_detail.publish_time,
        "categoryId": new_detail.category_id,
        "views": new_detail.views,
    }for new_detail in related_news1]