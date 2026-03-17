from functools import lru_cache
from typing import Optional, Self

from django.forms import IntegerField
from service_objects.errors import NotFound
from service_objects.fields import ModelField
from service_objects.services import ServiceWithResult

from photition_models.models.photo.materialized_views import PhotoStats
from photition_models.models.photo.photo_model import Photo
from photition_models.models.photo.vote_model import Vote
from photition_models.models.user.photition_user_model import PhotitionUser


class VoteService(ServiceWithResult):
    id = IntegerField()
    user = ModelField(PhotitionUser)

    custom_validations = ["photo_presence"]

    def process(self) -> Self:
        self.run_custom_validations()

        if self.is_valid():
            self.vote()

        return self

    def vote(self) -> None:
        prev_vote = self.prev_vote()

        if prev_vote is not None:
            prev_vote.delete()
        else:
            Vote.objects.create(photo=self._photo, user=self._user)

        PhotoStats.refresh()

    @property
    @lru_cache()
    def _photo(self) -> Optional[Photo]:
        return Photo.objects.safe_get(id=self.cleaned_data["id"])

    def prev_vote(self) -> Optional[Vote]:
        return Vote.objects.safe_get(photo=self._photo, user=self._user)

    @property
    @lru_cache()
    def _user(self) -> PhotitionUser:
        return self.cleaned_data["user"]

    def photo_presence(self) -> None:
        photo = self._photo

        if photo is None:
            self.add_error("id", NotFound("Фото отсутствует"))
