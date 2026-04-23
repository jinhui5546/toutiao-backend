from datetime import datetime
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import Integer, DateTime, ForeignKey
from models.news import Base  # 使用共享的Base类


class RelatedNews(Base):
    __tablename__ = 'related_news'
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True, comment="关联ID")
    news_id: Mapped[int] = mapped_column(Integer, ForeignKey('news.id'), nullable=False, comment="新闻ID")
    related_news_id: Mapped[int] = mapped_column(Integer, ForeignKey('news.id'), nullable=False, comment="相关新闻ID")
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now, comment="创建时间")
    
    def __repr__(self):
        return f"<RelatedNews(id={self.id}, news_id={self.news_id}, related_news_id={self.related_news_id})>"
