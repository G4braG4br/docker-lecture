from typing import Self

from service_objects.fields import ModelField
from service_objects.services import ServiceWithResult

from photition_models.models.user.photition_session_model import PhotitionSession
from photition_models.models.user.photition_user_model import PhotitionUser


class LogoutService(ServiceWithResult):
    user = ModelField(PhotitionUser)

    def process(self) -> Self:
        self.run_custom_validations()
        if self.is_valid():
            self.logout()
        return self

    def logout(self) -> None:
        token = self._token
        if token is not None:
            token.delete()
        return None

    @property
    def _user(self) -> PhotitionUser:
        return self.cleaned_data.get("user")

    @property
    def _token(self) -> PhotitionSession:
        return PhotitionSession.objects.safe_get(user=self._user)
