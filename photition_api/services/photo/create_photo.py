from typing import Self

from django.forms import CharField, FileField
from service_objects.errors import ValidationError
from service_objects.fields import ModelField
from service_objects.services import ServiceWithResult

from photition_api.utils.validate_file import validate_file
from photition_models.models.photo.materialized_views import PhotoStats
from photition_models.models.photo.photo_model import Photo
from photition_models.models.user.photition_user_model import PhotitionUser


class CreatePhotoService(ServiceWithResult):
    user = ModelField(PhotitionUser)
    photo = FileField()
    title = CharField()
    description = CharField(required=False)

    custom_validations = ["validate"]

    def process(self) -> Self:
        self.run_custom_validations()

        if self.is_valid():
            self.result = self.create_photo()

        return self

    def create_photo(self) -> Photo:
        new_photo = Photo(
            photo=self.cleaned_data["photo"],
            title=self.cleaned_data["title"],
            description=self.cleaned_data.get("description"),
            author=self._user,
        )

        new_photo.save()
        PhotoStats.refresh()
        return new_photo

    @property
    def _user(self) -> PhotitionUser:
        return self.cleaned_data["user"]

    def validate(self) -> None:
        photo = self.cleaned_data["photo"]

        if not validate_file(photo):
            self.add_error("photo", ValidationError("Недопустимый файл"))
