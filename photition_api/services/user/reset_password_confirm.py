from functools import lru_cache
from typing import Optional, Self

from decouple import config
from django.contrib.auth.tokens import default_token_generator
from django.forms import CharField
from django.utils.http import urlsafe_base64_decode
from service_objects.services import ServiceWithResult

from photition_models.models import PhotitionUser

DEFAULT_FROM_EMAIL = config("DEFAULT_FROM_EMAIL", "default")


class ResetPasswordConfirmService(ServiceWithResult):
    encoded_pk = CharField()
    token = CharField()
    new_password = CharField(min_length=8, max_length=32)

    custom_validations = [
        "check_user",
        "check_token",
    ]

    def process(self) -> Self:
        self.run_custom_validations()
        if self.is_valid():
            self.change_password()

        return self

    def change_password(self) -> None:
        self._user.set_password(self.cleaned_data["new_password"])
        self._user.save()

    def check_token(self) -> None:
        if not default_token_generator.check_token(
            self._user, self.cleaned_data["token"]
        ):
            self.add_error("token", "Неверный токен")

    def check_user(self) -> None:
        if self._user is None:
            self.add_error("user", "Пользователь не найден")

    @property
    def _pk(self) -> str:
        return urlsafe_base64_decode(self.cleaned_data["encoded_pk"]).decode()

    @property
    @lru_cache
    def _user(self) -> Optional[PhotitionUser]:
        return PhotitionUser.objects.safe_get(pk=self._pk)
