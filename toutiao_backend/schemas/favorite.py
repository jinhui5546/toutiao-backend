from pydantic import BaseModel
from datetime import datetime
from typing import Optional, List


# 收藏请求
class FavoriteRequest(BaseModel):
    newsId: int


# 收藏响应
class FavoriteResponse(BaseModel):
    id: int
    userId: int
    newsId: int
    createTime: datetime
    
    class Config:
        from_attributes = True


# 收藏列表项
class FavoriteListItem(BaseModel):
    id: int
    title: str
    description: str = ""
    image: str = ""
    author: str = ""
    publishTime: datetime
    categoryId: int
    views: int
    favoriteTime: datetime


# 收藏列表响应
class FavoriteListResponse(BaseModel):
    list: List[FavoriteListItem]
    total: int
    hasMore: bool


# 收藏状态检查响应
class FavoriteCheckResponse(BaseModel):
    isFavorite: bool
