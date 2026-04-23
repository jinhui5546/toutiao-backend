from fastapi import APIRouter, Depends, HTTPException, status, Query, Path
from sqlalchemy.ext.asyncio import AsyncSession
import traceback

from crud.history import (
    add_history,
    get_history_list,
    delete_history,
    clear_all_history
)
from schemas.history import HistoryRequest
from config.db_config import get_db
from utils.auth import get_current_user
from models.user import User

router = APIRouter(prefix="/api/history", tags=["history"])


@router.post("/add")
async def add_view_history(
    request: HistoryRequest,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """添加浏览记录"""
    try:
        print(f"添加浏览历史: user_id={current_user.id}, news_id={request.newsId}")
        history = await add_history(db, current_user.id, request.newsId)
        print(f"浏览历史添加成功: history_id={history.id}")
        
        return {
            "code": 200,
            "message": "添加成功",
            "data": {
                "id": history.id,
                "userId": history.user_id,
                "newsId": history.news_id,
                "viewTime": history.created_at
            }
        }
    except Exception as e:
        print(f"添加浏览历史失败: {str(e)}")
        traceback.print_exc()
        raise


@router.get("/list")
async def get_history(
    page: int = Query(1, ge=1, description="页码"),
    pageSize: int = Query(10, ge=1, le=100, alias="pageSize", description="每页条数"),
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """获取浏览历史列表"""
    try:
        print(f"获取浏览历史: user_id={current_user.id}, page={page}, pageSize={pageSize}")
        histories, total = await get_history_list(db, current_user.id, page, pageSize)
        print(f"浏览历史查询结果: {len(histories)}条, total={total}")
        
        # 格式化返回数据
        history_list = []
        for hist, news in histories:
            history_list.append({
                "id": news.id,
                "title": news.title,
                "description": news.description or "",
                "image": news.image or "",
                "author": news.author or "",
                "publishTime": news.publish_time,
                "categoryId": news.category_id,
                "views": news.views,
                "viewTime": hist.created_at
            })
        
        has_more = (page - 1) * pageSize + len(history_list) < total
        
        return {
            "code": 200,
            "message": "success",
            "data": {
                "list": history_list,
                "total": total,
                "hasMore": has_more
            }
        }
    except Exception as e:
        print(f"获取浏览历史失败: {str(e)}")
        traceback.print_exc()
        raise


@router.delete("/delete/{history_id}")
async def delete_history_record(
    history_id: int = Path(..., description="历史记录ID"),
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """删除单条浏览记录"""
    success = await delete_history(db, history_id, current_user.id)
    
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="历史记录不存在"
        )
    
    return {
        "code": 200,
        "message": "删除成功",
        "data": None
    }


@router.delete("/clear")
async def clear_history(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """清空浏览历史"""
    count = await clear_all_history(db, current_user.id)
    
    return {
        "code": 200,
        "message": "清空成功",
        "data": None
    }
