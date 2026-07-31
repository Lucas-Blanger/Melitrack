from celery import Celery
from app.config import settings

celery = Celery(
    "ml-service",
    broker=settings.REDIS_URL,
    backend=settings.REDIS_URL,
    include=["app.tasks.analysis_tasks"],
)

celery.conf.update(
    task_routes={"app.tasks.analysis_tasks.analyze_hive_photo": {"queue": "ml"}},
    task_serializer="json",
    result_serializer="json",
    accept_content=["json"],
    timezone="America/Sao_Paulo",
)
