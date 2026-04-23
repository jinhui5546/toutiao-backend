from datetime import datetime
from typing import Optional

from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import Integer, DateTime, ForeignKey
from models.news import Base  # 使用共享的Base类


class History(Base):
    __tablename__ = 'history'
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True, comment="历史记录ID")
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey('user.id'), nullable=False, comment="用户ID")
    news_id: Mapped[int] = mapped_column(Integer, ForeignKey('news.id'), nullable=False, comment="新闻ID")
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now, comment="浏览时间")
    
    def __repr__(self):
        return f"<History(id={self.id}, user_id={self.user_id}, news_id={self.news_id})>"
