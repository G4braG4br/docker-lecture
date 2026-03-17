from django.db import models

from photition_models.models.user.managers.photition_manager import PhotitionManager


class PhotitionSession(models.Model):

    objects = PhotitionManager.as_manager()

    user = models.ForeignKey(
        "photition_models.PhotitionUser",
        on_delete=models.CASCADE,
        related_name="sessions",
        related_query_name="session"
    )
    session_token = models.TextField(
        null=False,
        unique=True,
    )
    expires_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.user
