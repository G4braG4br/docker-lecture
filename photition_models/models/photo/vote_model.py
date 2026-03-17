from django.db import models

from photition_models.models import PhotitionUser
from photition_models.models.photo.photo_model import Photo
from photition_models.models.user.managers.photition_manager import PhotitionManager


class Vote(models.Model):
    objects = PhotitionManager.as_manager()

    user = models.ForeignKey("photition_models.PhotitionUser", on_delete=models.CASCADE)
    photo = models.ForeignKey("photition_models.Photo", on_delete=models.CASCADE)
