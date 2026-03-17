from celery import shared_task
from django.utils import timezone

from photition_models.models.photo.photo_model import Photo


@shared_task
def photo_expired_task():
    queryset = Photo.objects.filter(
        will_deleted_in__lte=timezone.now(), will_deleted_in__isnull=False
    )
    queryset.delete()
