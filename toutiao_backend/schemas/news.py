from pydantic import BaseModel
from datetime import datetime
from typing import Optional, List


# 新闻分类响应
class CategoryResponse(BaseModel):
    id: int
    name: str
    sort_order: int
    
    class Config:
        from_attributes = True


# 新闻列表项响应
class NewsListItem(BaseModel):
    id: int
    title: str
    description: Optional[str] = None
    image: Optional[str] = None
    author: Optional[str] = None
    category_id: int
    views: int
    publish_time: datetime
    
    class Config:
        from_attributes = True


# 新闻详情响应
class NewsDetailResponse(BaseModel):
    id: int
    title: str
    content: str
    image: Optional[str] = None
    author: Optional[str] = None
    publishTime: datetime
    categoryId: int
    views: int
    relatedNews: List[NewsListItem] = []


# 新闻列表响应
class NewsListResponse(BaseModel):
    list: List[NewsListItem]
    total: int
    hasMore: bool
