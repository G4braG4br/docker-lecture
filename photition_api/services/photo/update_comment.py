from functools import lru_cache
from typing import Optional, Self

from django.forms import CharField, IntegerField
from service_objects.errors import NotFound
from service_objects.services import ServiceWithResult

from photition_models.models.comment.models import Comment


class UpdateCommentService(ServiceWithResult):
    id = IntegerField()
    comment = CharField()

    custom_validations = ["comment_presence"]

    def process(self) -> Self:
        self.run_custom_validations()

        if self.is_valid():
            self.result = self.update_comment()

        return self

    def update_comment(self) -> Comment:
        self._comment.comment = self.cleaned_data["comment"]
        self._comment.save()
        return self._comment

    @property
    @lru_cache()
    def _comment(self) -> Optional[Comment]:
        return Comment.objects.with_prefetch_replies().safe_get(
            id=self.cleaned_data["id"]
        )

    def comment_presence(self) -> None:
        if self._comment is None:
            self.add_error("id", NotFound("Комментарий отсутствует"))
