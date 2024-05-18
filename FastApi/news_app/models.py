from sqlalchemy import Column, Integer, String, DateTime
from database import Base

class NewsArticle(Base):
    __tablename__ = 'news_articles'

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255))
    description = Column(String)
    published_at = Column(DateTime)

