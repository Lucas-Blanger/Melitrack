from celery import Celery

from app.core.logger import get_logger
from app.config import settings

logger = get_logger(__name__)

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
    worker_hijack_root_logger=False,
)
