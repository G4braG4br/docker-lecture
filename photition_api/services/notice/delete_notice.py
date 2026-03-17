from functools import lru_cache
from typing import Self

from django.forms import IntegerField
from service_objects.fields import ModelField
from service_objects.services import ServiceWithResult

from photition_models.models.notice.notice_status_model import NoticeStatus
from photition_models.models.user.photition_user_model import PhotitionUser


class DeleteNoticeService(ServiceWithResult):
    id = IntegerField()
    user = ModelField(PhotitionUser)

    def process(self) -> Self:
        self.delete_notice()
        return self

    def delete_notice(self):
        self._notice.is_closed = True
        self._notice.save()

    @property
    @lru_cache()
    def _notice(self):
        return NoticeStatus.objects.get(
            notice_id=self.cleaned_data["id"], user=self._user
        )

    @property
    def _user(self):
        return self.cleaned_data["user"]
