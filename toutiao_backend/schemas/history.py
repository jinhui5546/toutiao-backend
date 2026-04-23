from pydantic import BaseModel
from datetime import datetime
from typing import Optional, List


# 历史记录添加请求
class HistoryRequest(BaseModel):
    newsId: int


# 历史记录响应
class HistoryResponse(BaseModel):
    id: int
    userId: int
    newsId: int
    viewTime: datetime
    
    class Config:
        from_attributes = True


# 历史记录列表项
class HistoryListItem(BaseModel):
    id: int
    title: str
    description: str = ""
    image: str = ""
    author: str = ""
    publishTime: datetime
    categoryId: int
    views: int
    viewTime: datetime


# 历史记录列表响应
class HistoryListResponse(BaseModel):
    list: List[HistoryListItem]
    total: int
    hasMore: bool
