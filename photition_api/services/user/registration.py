from datetime import datetime, timedelta
from typing import Self

from decouple import config
from django.db import IntegrityError, transaction
from django.forms import CharField, EmailField
from service_objects.errors import ValidationError
from service_objects.services import ServiceWithResult

from photition.settings.django import SESSION_TOKEN_EXPIRES
from photition_api.utils.generate_token import generate_token
from photition_models.models.user.photition_session_model import PhotitionSession
from photition_models.models.user.photition_user_model import PhotitionUser


class RegistrationService(ServiceWithResult):
    username = CharField()
    email = EmailField()
    password = CharField()

    custom_validations = ["check_email", "check_username"]

    def process(self) -> Self:
        self.run_custom_validations()
        if self.is_valid():
            self.create_user()
        return self

    def create_user(self) -> PhotitionUser | None:
        try:
            with transaction.atomic():
                user = PhotitionUser(
                    username=self.cleaned_data["username"],
                    email=self.cleaned_data["email"],
                )
                user.set_password(self.cleaned_data["password"])
                session_token = generate_token()
                token = PhotitionSession(
                    session_token=session_token,
                    expires_at=datetime.now() + timedelta(days=SESSION_TOKEN_EXPIRES),
                    user=user,
                )
                user.save()
                token.save()

                self.result = user
                return user
        except IntegrityError:
            self.add_error(
                None, ValidationError(message="Ошибка при создании пользователя")
            )

    def check_email(self) -> None:
        user_by_email = PhotitionUser.objects.filter(
            email=self.cleaned_data["email"]
        ).exists()
        if user_by_email:
            self.add_error(
                "email",
                ValidationError(
                    message="Пользователь с таким email уже зарегистрирован",
                ),
            )

    def check_username(self) -> None:
        user_by_username = PhotitionUser.objects.filter(
            username=self.cleaned_data["username"]
        ).exists()
        if user_by_username:
            self.add_error(
                "username",
                ValidationError(
                    message="Пользователь с таким username уже зарегистрирован",
                ),
            )
