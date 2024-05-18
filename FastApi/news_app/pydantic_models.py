from pydantic import BaseModel
from datetime import datetime

class NewsArticleBase(BaseModel):
    title: str
    description: str

class NewsArticleCreate(NewsArticleBase):
    pass

class NewsArticle(NewsArticleBase):
    id: int
    published_at:datetime

    class Config:
        orm_mode = True
