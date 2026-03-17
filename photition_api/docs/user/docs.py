from rest_framework import status
from service_objects_autodocs.auto_parameters_spectacular import (
    prepare_parameters_for_docs,
    prepare_request_body_for_docs,
)
from service_objects_autodocs.exceptions import (
    get_authentication_failed_yasg_response,
    get_not_found_error_yasg_response,
    get_validation_error_yasg_response,
)

from photition_api.serializers.user import SessionTokenSerializer, UserSerializer
from photition_api.services.user import (
    GetUserService,
    LoginService,
    LogoutService,
    RefreshService,
    RegistrationService,
    UpdateUserService,
)

registration_doc: dict = {
    "tags": [
        "Users",
    ],
    "summary": "User Registration",
    "request": prepare_request_body_for_docs(RegistrationService),
    "responses": {
        status.HTTP_201_CREATED: UserSerializer,
        status.HTTP_400_BAD_REQUEST: get_validation_error_yasg_response,
    },
}

login_doc: dict = {
    "tags": [
        "Users",
    ],
    "summary": "User Login",
    "request": prepare_request_body_for_docs(LoginService),
    "responses": {
        status.HTTP_200_OK: UserSerializer,
        status.HTTP_400_BAD_REQUEST: get_authentication_failed_yasg_response,
    },
}

logout_doc: dict = {
    "tags": [
        "Users",
    ],
    "summary": "User Logout",
    "request": prepare_request_body_for_docs(LogoutService, exclude=("user",)),
    "responses": {
        status.HTTP_200_OK: None,
        status.HTTP_401_UNAUTHORIZED: get_authentication_failed_yasg_response,
    },
}

refresh_doc: dict = {
    "tags": [
        "Users",
    ],
    "summary": "User refresh session token ",
    "request": prepare_request_body_for_docs(RefreshService, exclude=("user",)),
    "responses": {
        status.HTTP_200_OK: SessionTokenSerializer,
        status.HTTP_401_UNAUTHORIZED: get_authentication_failed_yasg_response,
    },
}

get_user_doc: dict = {
    "tags": [
        "Users",
    ],
    "summary": "Get current user ",
    "request": prepare_parameters_for_docs(GetUserService, exclude=("user",)),
    "responses": {
        status.HTTP_200_OK: UserSerializer,
        status.HTTP_401_UNAUTHORIZED: get_authentication_failed_yasg_response,
    },
}

update_user_doc: dict = {
    "tags": [
        "Users",
    ],
    "summary": "Update user",
    "request": prepare_request_body_for_docs(
        UpdateUserService,
        exclude=("user",),
        body_data_types=("multipart/form-data",),
    ),
    "responses": {
        status.HTTP_200_OK: UserSerializer,
        status.HTTP_401_UNAUTHORIZED: get_authentication_failed_yasg_response,
    },
}
