from celery import Celery
from celery.schedules import crontab
from tasks import fetch_news_from_api

celery_app = Celery('tasks', broker='redis://localhost:6379/0')

celery_app.conf.beat_schedule = {
    'fetch-news-every-minute': {
        'task': 'tasks.fetch_news_from_api',
        'schedule': crontab(minute='*'),
    },
}

celery_app.conf.timezone = 'UTC'
