from django.db import models
from django.utils.translation import gettext_lazy as _

from photition_models.models.comment.managers import CommentManager


class Comment(models.Model):
    objects = CommentManager.as_manager()

    comment = models.TextField(
        max_length=100,
        verbose_name=_("Comment"),
        help_text=_("Comment text"),
    )
    photo = models.ForeignKey(
        "photition_models.Photo",
        on_delete=models.CASCADE,
        related_name="comments",
        related_query_name="comment",
        verbose_name=_("Photo"),
        help_text=_("Photo"),
    )
    author = models.ForeignKey(
        "photition_models.PhotitionUser",
        on_delete=models.CASCADE,
        related_name="comments",
        related_query_name="comment",
        verbose_name=_("Author"),
        help_text=_("Author"),
    )
    belongs_to = models.ForeignKey(
        "self",
        on_delete=models.CASCADE,
        related_name="belongs",
        related_query_name="belong",
        null=True,
        blank=True,
        verbose_name=_("Belongs to"),
        help_text=_("Belongs to"),
    )
    answer_to = models.ForeignKey(
        "self",
        on_delete=models.CASCADE,
        related_name="answers",
        related_query_name="answer",
        null=True,
        blank=True,
        verbose_name=_("Answer to"),
        help_text=_("Answer to"),
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_("Created at"),
        help_text=_("Created at"),
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name=_("Updated at"),
        help_text=_("Updated at"),
    )
    is_deleted = models.BooleanField(
        default=False,
        verbose_name=_("Is deleted"),
        help_text=_("Is deleted"),
    )

    def __str__(self):
        return self.comment

    class Meta:
        verbose_name = _("Comment")
        verbose_name_plural = _("Comments")
