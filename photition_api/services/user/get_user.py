from typing import Self

from service_objects.fields import ModelField
from service_objects.services import ServiceWithResult

from photition_models.models.user.photition_user_model import PhotitionUser


class GetUserService(ServiceWithResult):
    user = ModelField(PhotitionUser)

    def process(self) -> Self:
        self.run_custom_validations()
        if self.is_valid():
            self.result = self.get_user()
        return self

    def get_user(self) -> PhotitionUser:
        return self._user

    @property
    def _user(self) -> PhotitionUser:
        return self.cleaned_data.get("user")
