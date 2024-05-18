import logging
from celery import Celery
import requests
from sqlalchemy.orm import Session
from datetime import datetime
from database import SessionLocal
from models import NewsArticle

logger = logging.getLogger(__name__)

celery_app = Celery('tasks', broker='redis://localhost:6379/0')

@celery_app.task
def fetch_news_from_api():
    logger.info("Starting fetch_news_from_api task")

    news_api_url = 'https://newsapi.org/v2/top-headlines'
    params = {
        'country': 'us',
        'apiKey': '19d227734ba94c28b647178ac9e81a11'
    }
    response = requests.get(news_api_url, params=params)
    news_data = response.json()

    logger.info(f"Fetched {len(news_data.get('articles', []))} articles")

    db = SessionLocal()
    try:
        for article in news_data.get('articles', []):
            news_article = NewsArticle(
                title=article.get('title', ''),
                description=article.get('description', ''),
                published_at=datetime.strptime(article.get('publishedAt', ''), '%Y-%m-%dT%H:%M:%SZ') if article.get('publishedAt') else None
            )
            
        db.commit()

        logger.info("Data committed to the database")

    except Exception as e:
        logger.error(f"Error occurred: {e}")
        db.rollback()
    finally:
        db.close()
    return news_data



