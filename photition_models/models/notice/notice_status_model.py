from django.db import models

from photition_models.models import PhotitionUser
from photition_models.models.notice.notice_model import Notice
from photition_models.models.user.managers.photition_manager import PhotitionManager


class NoticeStatus(models.Model):
    objects = PhotitionManager.as_manager()
    user = models.ForeignKey(PhotitionUser, on_delete=models.CASCADE)
    notice = models.ForeignKey(
        "photition_models.Notice",
        on_delete=models.CASCADE,
        related_name="notice_statuses",
        related_query_name="notice_status",
    )
    is_closed = models.BooleanField(default=False)
