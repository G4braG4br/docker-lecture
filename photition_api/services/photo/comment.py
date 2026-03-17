from typing import Optional

from django.forms import CharField, IntegerField
from rest_framework.exceptions import NotFound
from service_objects.fields import ModelField
from service_objects.services import ServiceWithResult
from typing_extensions import Self

from photition_models.models.comment.models import Comment
from photition_models.models.photo.materialized_views import PhotoStats
from photition_models.models.photo.photo_model import Photo
from photition_models.models.user.photition_user_model import PhotitionUser


class CommentService(ServiceWithResult):
    id = IntegerField()
    user = ModelField(PhotitionUser)
    comment = CharField()
    answer_to = IntegerField(required=False)

    custom_validations = ["photo_presence"]

    def process(self) -> Self:
        self.run_custom_validations()

        if self.is_valid():
            self.result = self.create_comment()

        return self

    def create_comment(self) -> Comment:
        photo = self._photo
        user = self._user

        new_comment = Comment(
            photo=photo,
            author=user,
            comment=self.cleaned_data["comment"],
        )

        self.set_answer(new_comment)

        new_comment.save()
        PhotoStats.refresh()
        return new_comment

    @property
    def _photo(self) -> Optional[Photo]:
        return Photo.objects.safe_get(id=self.cleaned_data["id"])

    @property
    def _user(self) -> PhotitionUser:
        return self.cleaned_data["user"]

    def set_answer(self, new_comment):
        answer = self.cleaned_data.get("answer_to")

        if answer is not None:
            target = Comment.objects.safe_get(id=answer)
            if target is not None:
                new_comment.answer_to = target
                if target.belongs_to is not None:
                    new_comment.belongs_to = target.belongs_to
                else:
                    new_comment.belongs_to = target

    def photo_presence(self) -> None:
        photo = self._photo

        if photo is None:
            self.add_error("id", NotFound("Фото отсутствует"))
