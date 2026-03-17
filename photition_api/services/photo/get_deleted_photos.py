from functools import lru_cache
from typing import Self

from django.utils import timezone
from service_objects.fields import ModelField
from service_objects.services import ServiceWithResult

from photition_models.models.photo.photo_model import Photo
from photition_models.models.user.photition_user_model import PhotitionUser


class GetDeletedPhotos(ServiceWithResult):
    user = ModelField(PhotitionUser)

    def process(self) -> Self:
        if self.is_valid():
            self.result = self.get_photos()

        return self

    def get_photos(self) -> Photo:
        return Photo.objects.filter(
            is_deleted=True, author=self._user, will_deleted_in__gte=timezone.now()
        )

    @property
    @lru_cache()
    def _user(self) -> PhotitionUser:
        return self.cleaned_data["user"]
