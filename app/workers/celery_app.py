from celery import Celery

from app.core.config import settings


celery_app = Celery(
    "omnicopy",
    broker=settings.CELERY_BROKER_URL,
    include=[
        "app.workers.tasks"
    ]
)


celery_app.conf.update(
    task_track_started=True,
    broker_connection_retry_on_startup=True
)
