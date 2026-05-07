from celery import Celery
import app.models
import ssl
from app.core.config import REDIS_URL

celery_app = Celery("docquery", broker=REDIS_URL, backend=REDIS_URL)

celery_app.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="UTC",
    enable_utc=True,
    worker_prefetch_multiplier=1,
    task_acks_late=True,
)
celery_app.conf.broker_use_ssl = {"ssl_cert_reqs": ssl.CERT_NONE}

celery_app.conf.redis_backend_use_ssl = {"ssl_cert_reqs": ssl.CERT_NONE}

celery_app.conf.imports = ("app.tasks.document_tasks",)
