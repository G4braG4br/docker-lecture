from datetime import datetime, timedelta
from typing import Self

from decouple import config
from django.forms import CharField, EmailField
from service_objects.errors import ValidationError
from service_objects.services import ServiceWithResult

from photition.settings.django import SESSION_TOKEN_EXPIRES
from photition_api.utils.generate_token import generate_token
from photition_models.models.user.photition_session_model import PhotitionSession
from photition_models.models.user.photition_user_model import PhotitionUser


class LoginService(ServiceWithResult):
    email = EmailField()
    password = CharField()

    custom_validations = ["check_email", "check_password"]

    def process(self) -> Self:
        self.run_custom_validations()
        if self.is_valid():
            self.result = self.login_user()
        return self

    def login_user(self) -> PhotitionUser:
        token = self._token
        if token is None:
            new_token = PhotitionSession(
                session_token=generate_token(),
                expires_at=datetime.now() + timedelta(days=SESSION_TOKEN_EXPIRES),
                user=self._user,
            )
            new_token.save()
        else:
            token.session_token = generate_token()
            token.expires_at = datetime.now() + timedelta(days=SESSION_TOKEN_EXPIRES)
            token.save()

        return self._user

    @property
    def _user(self) -> PhotitionUser:
        return PhotitionUser.objects.safe_get(email=self.cleaned_data["email"])

    @property
    def _token(self) -> PhotitionSession:
        return PhotitionSession.objects.safe_get(user=self._user)

    def check_email(self) -> None:
        if self._user is None:
            self.add_error(
                "email",
                ValidationError(
                    message="Пользователь с таким email отсутствует",
                ),
            )

    def check_password(self) -> None:
        if self._user is not None and not self._user.check_password(
            self.cleaned_data["password"]
        ):
            self.add_error(
                "password",
                ValidationError(
                    message="Неверный пароль",
                ),
            )
