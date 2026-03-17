from typing import Self

from service_objects.fields import ModelField
from service_objects.services import ServiceWithResult

from photition_models.models import Notice
from photition_models.models.user.photition_user_model import PhotitionUser


class GetNoticesService(ServiceWithResult):
    user = ModelField(PhotitionUser)

    def process(self) -> Self:
        self.result = self.get_notices()
        return self

    def get_notices(self):
        return (
            Notice.objects.filter(
                notice_status__is_closed=False,
                notice_status__user=self._user,
            )
            .distinct()
            .order_by("id")
        )

    @property
    def _user(self):
        return self.cleaned_data["user"]
