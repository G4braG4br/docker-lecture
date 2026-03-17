from functools import lru_cache
from typing import Self

from django.forms import CharField, EmailField, FileField
from service_objects.errors import ValidationError
from service_objects.fields import ModelField
from service_objects.services import ServiceWithResult

from photition_api.utils.sort_data import sort_data
from photition_api.utils.validate_file import validate_file
from photition_models.models.user.photition_user_model import PhotitionUser


class UpdateUserService(ServiceWithResult):
    user = ModelField(PhotitionUser)
    email = EmailField(required=False)
    username = CharField(required=False)
    password = CharField(required=False, min_length=8)
    avatar = FileField(required=False)
    REQUIRED = []

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.FIELDS = dict()
        self.FILE_FIELDS = dict()

    custom_validations = [
        "check_required_fields",
        "check_file_fields",
        "check_username",
        "check_email",
        "check_password",
    ]

    def process(self) -> Self:
        sort_data(self.data, self.FIELDS, self.FILE_FIELDS)

        self.run_custom_validations()
        if self.is_valid():
            self.result = self.update_user()

        return self

    def update_user(self) -> PhotitionUser:
        self.update_fields()
        self.update_file_fields()
        return self._user

    def update_fields(self) -> None:
        for key, value in self.FIELDS.items():
            if hasattr(self._user, key):
                if key == "password":
                    self._user.set_password(value)
                else:
                    setattr(self._user, key, value)
        self._user.save()

    def update_file_fields(self):
        for key, value in self.FILE_FIELDS.items():
            if hasattr(self._user, key):
                prev_value = getattr(self._user, key)
                prev_value.delete()
                setattr(self._user, key, value)
        self._user.save()

    @property
    @lru_cache()
    def _user(self) -> PhotitionUser:
        return self.cleaned_data.get("user")

    def check_required_fields(self) -> None:
        different = set(self.REQUIRED) - set(self.data.keys())
        if len(different) > 0:
            for item in different:
                self.add_error(item, ValidationError(message=item + " отсутствует"))

    def check_file_fields(self) -> None:
        for key, value in self.FILE_FIELDS.items():
            if not validate_file(value):
                self.add_error(
                    key,
                    ValidationError(
                        message="Не валидный файл",
                    ),
                )

    def check_username(self) -> None:
        username = self.data.get("username")
        if username is not None:
            is_not_exist = not PhotitionUser.objects.filter(username=username).exists()
            is_not_current = username != self._user.username
            if not is_not_exist and is_not_current:
                self.add_error(
                    username,
                    ValidationError(
                        message="Этот username уже занят",
                    ),
                )
                return
            if username == "":
                self.add_error(
                    username,
                    ValidationError(
                        message="Пустой username",
                    ),
                )

    def check_email(self) -> None:
        email = self.data.get("email")
        if email is not None:
            is_not_exist = not PhotitionUser.objects.filter(email=email).exists()
            is_not_current = email != self._user.email
            if not is_not_exist and is_not_current:
                self.add_error(
                    email,
                    ValidationError(
                        message="Этот email уже занят",
                    ),
                )
                return
            if email == "":
                self.add_error(
                    email,
                    ValidationError(
                        message="Пустой email",
                    ),
                )

    def check_password(self) -> None:
        password = self.data.get("password")
        if password is not None:
            if password == "":
                self.add_error(
                    password,
                    ValidationError(
                        message="Пустой пароль",
                    ),
                )
