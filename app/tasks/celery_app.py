from celery import Celery
from celery.schedules import crontab
from app.core.config import settings

celery_app = Celery(
    "worker",
    broker=settings.REDIS_URL,
    backend=settings.REDIS_URL,
    include=["app.tasks.worker"]
)

# Настройка расписания
celery_app.conf.beat_schedule = {
    "fetch-prices-every-minute": {
        "task": "app.tasks.worker.fetch_and_store_prices",
        "schedule": 60.0,  # Раз в 60 секунд
    },
}

celery_app.conf.timezone = "UTC"


