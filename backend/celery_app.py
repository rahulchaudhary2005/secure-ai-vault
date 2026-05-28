from celery import Celery

celery = Celery(

    "secure_ai_vault",

    broker="redis://localhost:6379/0",

    backend="redis://localhost:6379/0"
)

celery.conf.update(

    task_serializer="json",

    accept_content=["json"],

    result_serializer="json",

    timezone="UTC",

    enable_utc=True,

    task_track_started=True,

    task_time_limit=1800,

    task_acks_late=True,

    worker_prefetch_multiplier=1,

    broker_connection_retry_on_startup=True
)