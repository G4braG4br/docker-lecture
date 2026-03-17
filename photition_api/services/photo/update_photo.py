from functools import lru_cache
from typing import Optional, Self

from django.forms import CharField, FileField, IntegerField
from service_objects.errors import NotFound, ValidationError
from service_objects.services import ServiceWithResult

from photition_api.utils.sort_data import sort_data
from photition_api.utils.validate_file import validate_file
from photition_models.models.photo.photo_model import Photo


class UpdatePhotoService(ServiceWithResult):
    id = IntegerField()
    photo = FileField(required=False)
    title = CharField(required=False)
    description = CharField(required=False)
    REQUIRED = []

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.FIELDS = dict()
        self.FILE_FIELDS = dict()

    custom_validations = [
        "photo_presence",
        "check_required_fields",
        "check_file_fields",
        "check_description",
        "check_title",
    ]

    def process(self) -> Self:
        sort_data(self.data, self.FIELDS, self.FILE_FIELDS)
        self.run_custom_validations()

        if self.is_valid():
            self.result = self.update_photo()

        return self

    def update_photo(self) -> Photo:
        self.update_fields()
        self.update_file_fields()
        self._photo.roll_back()
        self._photo.save()
        return self._photo

    def update_fields(self) -> None:
        for key, value in self.FIELDS.items():
            if hasattr(self._photo, key):
                setattr(self._photo, key, value)
        self._photo.save()

    def update_file_fields(self):
        for key, value in self.FILE_FIELDS.items():
            if hasattr(self._photo, key):
                if key == "photo":
                    photo = getattr(self._photo, key)
                    prev_photo = getattr(self._photo, "prev_photo")
                    prev_photo.delete()
                    setattr(self._photo, "prev_photo", photo)
                    setattr(self._photo, key, value)
                else:
                    prev = getattr(self._photo, key)
                    prev.delete()
                    setattr(self._photo, key, value)
        self._photo.save()

    @property
    @lru_cache()
    def _photo(self) -> Optional[Photo]:
        return Photo.objects.with_prefetch_comments().safe_get(
            id=self.cleaned_data["id"]
        )

    def photo_presence(self) -> None:
        if self._photo is None:
            self.add_error("id", NotFound("Фото отсутствует"))

    def check_required_fields(self) -> None:
        different = set(self.REQUIRED) - set(self.data.keys())
        if len(different) > 0:
            for item in different:
                self.add_error(item, ValidationError(message=item + " отсутствует"))

    def check_file_fields(self) -> None:
        for key, value in self.FILE_FIELDS.items():
            if not validate_file(value):
                self.add_error(
                    key,
                    ValidationError(
                        message="Не валидный файл",
                    ),
                )

    def check_title(self) -> None:
        title = self.data.get("title")
        if title is not None:
            if title == "":
                self.add_error(
                    title,
                    ValidationError(
                        message="Пустой заголовок",
                    ),
                )

    def check_description(self) -> None:
        description = self.data.get("description")
        if description is not None:
            if description == "":
                self.add_error(
                    description,
                    ValidationError(
                        message="Пустое описание",
                    ),
                )
