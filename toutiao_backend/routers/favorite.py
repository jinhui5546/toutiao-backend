from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.ext.asyncio import AsyncSession
import traceback

from crud.favorite import (
    check_favorite,
    add_favorite,
    remove_favorite,
    get_favorite_list,
    clear_all_favorites
)
from schemas.favorite import FavoriteRequest
from config.db_config import get_db
from utils.auth import get_current_user
from models.user import User

router = APIRouter(prefix="/api/favorite", tags=["favorite"])


@router.get("/check")
async def check_news_favorite(
    newsId: int = Query(..., description="新闻ID"),
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """检查新闻收藏状态"""
    try:
        print(f"检查收藏状态: user_id={current_user.id}, news_id={newsId}")
        is_favorited = await check_favorite(db, current_user.id, newsId)
        print(f"收藏状态: {is_favorited}")
        
        return {
            "code": 200,
            "message": "success",
            "data": {
                "isFavorite": is_favorited
            }
        }
    except Exception as e:
        print(f"检查收藏状态失败: {str(e)}")
        traceback.print_exc()
        raise


@router.post("/add")
async def add_news_favorite(
    request: FavoriteRequest,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """添加收藏"""
    try:
        print(f"添加收藏: user_id={current_user.id}, news_id={request.newsId}")
        # 检查是否已收藏
        is_favorited = await check_favorite(db, current_user.id, request.newsId)
        if is_favorited:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="已经收藏过该新闻"
            )
        
        favorite = await add_favorite(db, current_user.id, request.newsId)
        print(f"收藏成功: favorite_id={favorite.id}")
        
        return {
            "code": 200,
            "message": "收藏成功",
            "data": {
                "id": favorite.id,
                "userId": favorite.user_id,
                "newsId": favorite.news_id,
                "createTime": favorite.created_at
            }
        }
    except HTTPException:
        raise
    except Exception as e:
        print(f"添加收藏失败: {str(e)}")
        traceback.print_exc()
        raise


@router.delete("/remove")
async def remove_news_favorite(
    newsId: int = Query(..., description="新闻ID"),
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """取消收藏"""
    success = await remove_favorite(db, current_user.id, newsId)
    
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="收藏记录不存在"
        )
    
    return {
        "code": 200,
        "message": "取消收藏成功",
        "data": None
    }


@router.get("/list")
async def get_favorites(
    page: int = Query(1, ge=1, description="页码"),
    pageSize: int = Query(10, ge=1, le=100, alias="pageSize", description="每页条数"),
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """获取收藏列表"""
    favorites, total = await get_favorite_list(db, current_user.id, page, pageSize)
    
    # 格式化返回数据
    favorite_list = []
    for fav, news in favorites:
        favorite_list.append({
            "id": news.id,
            "title": news.title,
            "description": news.description or "",
            "image": news.image or "",
            "author": news.author or "",
            "publishTime": news.publish_time,
            "categoryId": news.category_id,
            "views": news.views,
            "favoriteTime": fav.created_at
        })
    
    has_more = (page - 1) * pageSize + len(favorite_list) < total
    
    return {
        "code": 200,
        "message": "success",
        "data": {
            "list": favorite_list,
            "total": total,
            "hasMore": has_more
        }
    }


@router.delete("/clear")
async def clear_favorites(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """清空所有收藏"""
    count = await clear_all_favorites(db, current_user.id)
    
    return {
        "code": 200,
        "message": f"成功删除{count}条收藏记录",
        "data": None
    }
