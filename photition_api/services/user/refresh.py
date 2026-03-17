from datetime import datetime, timedelta
from typing import Self

from decouple import config
from service_objects.fields import ModelField
from service_objects.services import ServiceWithResult

from photition.settings.django import SESSION_TOKEN_EXPIRES
from photition_api.utils.generate_token import generate_token
from photition_models.models.user.photition_session_model import PhotitionSession
from photition_models.models.user.photition_user_model import PhotitionUser


class RefreshService(ServiceWithResult):
    user = ModelField(PhotitionUser)

    def process(self) -> Self:
        self.run_custom_validations()
        if self.is_valid():
            self.result = self.refresh()
        return self

    def refresh(self) -> PhotitionSession:
        token = self._token
        if token is not None:
            token.session_token = generate_token()
            token.expires_at = datetime.now() + timedelta(days=SESSION_TOKEN_EXPIRES)
            token.save()

            return token
        else:
            new_token = PhotitionSession(
                session_token=generate_token(),
                expires_at=datetime.now() + timedelta(days=SESSION_TOKEN_EXPIRES),
                user=self._user,
            )
            new_token.save()

            return new_token

    @property
    def _user(self) -> PhotitionUser:
        return self.cleaned_data.get("user")

    @property
    def _token(self) -> PhotitionSession:
        return PhotitionSession.objects.safe_get(user=self._user)
