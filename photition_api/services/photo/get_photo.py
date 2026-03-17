from typing import Optional, Self

from django.db.models import Exists
from django.forms import IntegerField
from service_objects.errors import NotFound
from service_objects.fields import ModelField
from service_objects.services import ServiceWithResult

from photition_models.models.photo.photo_model import Photo
from photition_models.models.photo.vote_model import Vote
from photition_models.models.user.photition_user_model import PhotitionUser


class GetPhotoService(ServiceWithResult):
    id = IntegerField()
    user = ModelField(PhotitionUser, required=False)

    custom_validations = ["photo_presence"]

    def process(self) -> Self:
        self.run_custom_validations()

        if self.is_valid:
            self.result = self.get_photo()

        return self

    def get_photo(self) -> Photo:
        return self._photo

    @property
    def _photo(self) -> Optional[Photo]:
        vote_sub_query = Vote.objects.filter(
            user=self._user, photo_id=self.cleaned_data["id"]
        )
        return (
            Photo.objects.with_prefetch_comments()
            .select_related("stat")
            .annotate(is_voted=Exists(vote_sub_query))
            .safe_get(id=self.cleaned_data["id"])
        )

    @property
    def _user(self) -> PhotitionUser:
        return self.cleaned_data.get("user")

    def photo_presence(self) -> None:
        photo = self._photo

        if photo is None:
            self.add_error("id", NotFound("Фото отсутствует"))
