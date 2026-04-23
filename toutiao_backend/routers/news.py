

from fastapi import APIRouter,Depends,Query,HTTPException
from crud.news import get_news, get_newlist, get_news_count, get_dtail, get_related_views, related_news
from sqlalchemy.ext.asyncio import AsyncSession
from config.db_config import get_db
from models.news import NewList

router = APIRouter(prefix="/api/news",tags=["news"])

@router.get("/categories")
async def get_categories(db:AsyncSession=Depends(get_db),skip:int=0,limit:int =10):
        categorys = await get_news(db,skip,limit)
        return {
            "code":200,
            "message":"获取新闻分类成功",
            "data":categorys
        }

@router.get("/list")
async def get_new_list(
        categoryld:int=Query(...,alias="categoryId"),
        page:int=1,
        pagesize:int=Query(10,le=100,alias="pageSize"),
        db : AsyncSession=Depends(get_db)):
    offset = (page-1)*pagesize
    new_lists = await get_newlist(db,categoryld,offset,pagesize)
    total = await get_news_count(db,categoryld)
    has_more = (offset+len(new_lists))<total
    return {
        "code":200,
        "message":"success",
        "data":{
            "list":new_lists,
            "total":total,
            "hasmore":has_more
        }
    }

@router.get("/detail")
async def get_detail(db:AsyncSession=Depends(get_db),news_id:int=Query(...,alias="id")):
    new_detail = await get_dtail(db,news_id)
    if not new_detail:
        raise HTTPException(status_code=404,detail="新闻不存在")
    views = await get_related_views(db,news_id)
    if not views:
        raise HTTPException(status_code=404,detail="新闻不存在")
    related_new = await related_news(db,news_id,new_detail.category_id)
    return {
        "code":200,
        "message":"sucess",
        "data":{
            "id":new_detail.id,
            "title":new_detail.title,
            "content": new_detail.content,
            "image":new_detail.image,
            "author":new_detail.author,
            "publishTime": new_detail.publish_time,
            "categoryId": new_detail.category_id,
            "views": new_detail.views,
            "relatedNews":related_new

            

        }


    }