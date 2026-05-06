from celery import Celery
import app.models
celery_app = Celery(
    "docquery",
    broker="redis://localhost:6379/0",
    backend="redis://localhost:6379/0"
)

celery_app.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="UTC",
    enable_utc=True,

    worker_prefetch_multiplier=1,
    task_acks_late=True,
)

celery_app.conf.imports = ("app.tasks.document_tasks",)