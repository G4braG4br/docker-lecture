from typing import Optional, Self

from django.forms import IntegerField
from service_objects.errors import NotFound
from service_objects.services import ServiceWithResult

from photition_models.models.comment.models import Comment
from photition_models.models.photo.materialized_views import PhotoStats


class DeleteCommentService(ServiceWithResult):
    id = IntegerField()

    custom_validations = ["comment_presence"]

    def process(self) -> Self:
        self.run_custom_validations()

        if self.is_valid():
            self.delete_comment()

        return self

    def delete_comment(self) -> None:
        comment = self._comment
        if not self.check_answered:
            comment.is_deleted = True
        comment.save()
        PhotoStats.refresh()

    @property
    def _comment(self) -> Optional[Comment]:
        return Comment.objects.safe_get(id=self.cleaned_data["id"])

    @property
    def check_answered(self) -> bool:
        return Comment.objects.filter(answer_to=self._comment).exists()

    def comment_presence(self) -> None:
        comment = self._comment

        if comment is None:
            self.add_error("id", NotFound("Комментарий отсутствует"))
