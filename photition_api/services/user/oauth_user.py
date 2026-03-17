from datetime import datetime, timedelta
from typing import Self

from decouple import config
from django.db import IntegrityError, transaction
from django.forms import CharField, EmailField
from service_objects.errors import ValidationError
from service_objects.services import ServiceOutcome, ServiceWithResult

from photition.settings.django import SESSION_TOKEN_EXPIRES
from photition_api.services.user import RegistrationService
from photition_api.utils.generate_token import generate_token
from photition_api.utils.save_remote_image import save_remote_image
from photition_models.models.user.photition_session_model import PhotitionSession
from photition_models.models.user.photition_user_model import PhotitionUser


class OAuthUserService(ServiceWithResult):
    username = CharField()
    email = EmailField()
    password = CharField()
    avatar = CharField(required=False)

    def process(self) -> Self:
        self.result = self.oauth_user()
        return self

    def oauth_user(self):
        try:
            photition_user = self.get_user()
            if photition_user is None:
                return self.create_user()
            return self.auth_user()

        except ValidationError:
            self.add_error(
                None, ValidationError(message="Ошибка при создании пользователя")
            )

    def auth_user(self):
        photition_user = self.get_user()
        self.update_avatar()
        token = PhotitionSession.objects.safe_get(user_id=photition_user.id)

        if token is None:
            token = PhotitionSession(
                session_token=generate_token(),
                expires_at=datetime.now() + timedelta(days=SESSION_TOKEN_EXPIRES),
                user=photition_user,
            )
        else:
            token.session_token = generate_token()
            token.expires_at = datetime.now() + timedelta(days=SESSION_TOKEN_EXPIRES)
        token.save()
        return token.session_token

    def update_avatar(self):
        avatar = self.cleaned_data.get("avatar")
        if avatar is not None:
            user = self.get_user()
            save_remote_image(user, avatar)

    def create_user(self):
        outcome = ServiceOutcome(
            RegistrationService,
            {
                "email": self.cleaned_data["email"],
                "username": self.cleaned_data["username"],
                "password": self.cleaned_data["password"],
            },
        )
        self.update_avatar()
        token = PhotitionSession.objects.safe_get(user_id=outcome.result.id)
        return token.session_token

    def get_user(self):
        return PhotitionUser.objects.safe_get(email=self.cleaned_data["email"])
