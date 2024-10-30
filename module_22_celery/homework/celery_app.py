from celery import Celery
from config import CELERY_BROKER_URL, CELERY_RESULT_BACKEND

def make_celery():
    celery = Celery(
        'tasks',
        broker=CELERY_BROKER_URL,
        backend=CELERY_RESULT_BACKEND,

    )

    return celery

celery = make_celery()
celery.autodiscover_tasks(['tasks'], force=True)
