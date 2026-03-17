from smtplib import SMTPException
from typing import Optional, Self

from decouple import config
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.forms import EmailField
from django.utils.http import urlsafe_base64_encode
from jwt.utils import force_bytes
from service_objects.services import ServiceWithResult

from photition_models.models import PhotitionUser

CLIENT_HOST = config("CLIENT_HOST", "test")
DEFAULT_FROM_EMAIL = config("DEFAULT_FROM_EMAIL", "default")


class ResetPasswordStartService(ServiceWithResult):
    email = EmailField()

    custom_validations = ["user_presence"]

    def process(self) -> Self:
        self.run_custom_validations()
        if self.is_valid():
            self.send_reset_mail()

        return self

    def send_reset_mail(self):
        try:
            send_mail(
                "Восстановление пароля аккаунта Photition",
                f"Для восстановления пароля перейдите по ссылке {self.generate_confirm_link()}",
                DEFAULT_FROM_EMAIL,
                [self._user.email],
            )
        except SMTPException:
            self.add_error("mail", "Ошибка при попытке восстановления пароля")

    def generate_confirm_link(self) -> str:
        token = default_token_generator.make_token(self._user)
        encoded_pk = urlsafe_base64_encode(force_bytes(str(self._user.pk)))
        link = f"{CLIENT_HOST}reset-password-confirm/{encoded_pk}/{token}"
        return link

    def user_presence(self) -> None:
        if self._user is None:
            self.add_error("email", "Пользователя с таким email не существует")

    @property
    def _user(self) -> Optional[PhotitionUser]:
        return PhotitionUser.objects.safe_get(email=self.cleaned_data["email"])
