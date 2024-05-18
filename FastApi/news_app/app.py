import logging
from fastapi import FastAPI, Depends , HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import inspect
from database import SessionLocal, engine
from models import Base, NewsArticle
from tasks import fetch_news_from_api
from pydantic_models import NewsArticleCreate
from datetime import datetime

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)




Base.metadata.create_all(bind=engine)

def create_app() -> FastAPI:
    app = FastAPI()

    @app.post("/fetch-news")
    def trigger_fetch_news():
        logger.info("Fetch News Celery Task Triggered")
        fetch_news_from_api.delay()
        return {"message": "Task triggered"}

    def get_db():
        db = SessionLocal()
        try:
            yield db
        finally:
            db.close()

    @app.get("/check-table")
    def check_table(db: Session = Depends(get_db)):
        logger.info("Check Table EndPoint Called")

        inspector = inspect(db.get_bind())
        tables = inspector.get_table_names()
        if 'news_articles' in tables:
            columns = inspector.get_columns('news_articles')
            column_info = {column['name']: column['type'] for column in columns}
            return {"exists": True, "columns": column_info}
        else:
            return {"exists": False}

    @app.get("/news")
    def get_news(db: Session = Depends(get_db)):
        logger.info("Get News EndPoint Called ")

        articles = db.query(NewsArticle).all()
        return articles
    
    @app.get("/news/{news_id}")
    def get_news_id(news_id:int,db:Session=Depends(get_db)):
        news = db.query(NewsArticle).filter(NewsArticle.id == news_id).first()
        if news is None:
            raise HTTPException(status_code=404,details="Not Found")
        return news

    @app.post("/news")
    def create_news(news:NewsArticleCreate,db:Session=Depends(get_db)):
        db_news = NewsArticle(**news.model_dump(),published_at=datetime.now())
        db.add(db_news)
        db.commit()
        db.refresh(db_news)
        return db_news

    return app
