from functools import lru_cache
from typing import Any, Optional, Self

from django.forms import CharField, IntegerField
from django_fsm import has_transition_perm
from service_objects.errors import NotFound, ValidationError
from service_objects.fields import ModelField
from service_objects.services import ServiceWithResult

from photition_models.models.photo.photo_model import Photo
from photition_models.models.user.photition_user_model import PhotitionUser


class ModeratePhoto(ServiceWithResult):
    id = IntegerField()
    user = ModelField(PhotitionUser)
    action = CharField()

    custom_validations = ["photo_presence", "can_proceed"]

    def process(self) -> Self:
        self.run_custom_validations()

        if self.is_valid:
            self.result = self.moderate_photo()

        return self

    def moderate_photo(self) -> Photo:
        self.execute_action()
        self._photo.save()
        return self._photo

    @property
    @lru_cache()
    def _photo(self) -> Optional[Photo]:
        return Photo.objects.with_prefetch_comments().safe_get(
            id=self.cleaned_data["id"]
        )

    @property
    def _property(self) -> Any:
        return getattr(self._photo, self.cleaned_data["action"])

    def execute_action(self) -> None:
        self._property()

    def photo_presence(self) -> None:
        photo = self._photo

        if photo is None:
            self.add_error("id", NotFound("Фото отсутствует"))

    def can_proceed(self) -> None:
        if not self.check_transitions():
            self.add_error(
                "id",
                ValidationError(
                    message="Доступ запрещен",
                ),
            )

    def check_transitions(self) -> bool:
        if self._property is not None:
            if has_transition_perm(self._property, self.cleaned_data["user"]):
                return True
        return False
