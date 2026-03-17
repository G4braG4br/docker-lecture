from photition.celery import app as celery_app
from photition_api.tasks.photo_expired_task import photo_expired_task

__all__ = ("celery_app",)
