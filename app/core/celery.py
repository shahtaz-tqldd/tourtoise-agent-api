from celery import Celery

from app.core.config import get_settings
settings = get_settings()

celery_app = Celery(
    "worker",
    broker=settings.celery_broker_url,
    backend=settings.celery_result_backend,
    include=[],
)

celery_app.conf.task_routes = {
    "tasks.*": {"queue": "default"},
}