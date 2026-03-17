from datetime import datetime, timedelta
from typing import Optional, Self

from decouple import config
from django.forms import IntegerField
from service_objects.errors import NotFound
from service_objects.services import ServiceWithResult

from photition_models.models.photo.photo_model import Photo

RESTORE_TIME = int(config("RESTORE_TIME", 3600))


class DeletePhotoService(ServiceWithResult):
    id = IntegerField()

    custom_validations = ["photo_presence"]

    def process(self) -> Self:
        self.run_custom_validations()

        if self.is_valid():
            self.delete_photo()

        return self

    def delete_photo(self) -> None:
        photo = self._photo
        photo.will_deleted_in = datetime.now() + timedelta(minutes=RESTORE_TIME)
        photo.is_deleted = True
        photo.save()

    @property
    def _photo(self) -> Optional[Photo]:
        return Photo.objects.safe_get(id=self.cleaned_data["id"])

    def photo_presence(self) -> None:
        photo = self._photo

        if photo is None:
            self.add_error("id", NotFound("Фото отсутствует"))
