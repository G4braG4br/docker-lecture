from functools import lru_cache
from typing import Optional, Self

from django.forms import IntegerField
from django.utils import timezone
from service_objects.errors import NotFound
from service_objects.services import ServiceWithResult

from photition_models.models.photo.photo_model import Photo


class RestorePhotoService(ServiceWithResult):
    id = IntegerField()

    custom_validations = ["photo_presence"]

    def process(self) -> Self:
        self.run_custom_validations()

        if self.is_valid():
            self.result = self.restore_photo()

        return self

    def restore_photo(self) -> Photo:
        photo = self._photo
        if photo.will_deleted_in is not None:
            if timezone.now() < photo.will_deleted_in:
                photo.roll_back()
                photo.will_deleted_in = None
        photo.save()
        return photo

    @property
    @lru_cache()
    def _photo(self) -> Optional[Photo]:
        return Photo.objects.with_prefetch_comments().safe_get(
            id=self.cleaned_data["id"]
        )

    def photo_presence(self) -> None:
        photo = self._photo

        if photo is None:
            self.add_error("id", NotFound("Фото отсутствует"))
