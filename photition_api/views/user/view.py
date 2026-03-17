from drf_spectacular.utils import extend_schema
from rest_framework.parsers import FormParser, MultiPartParser
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from service_objects.services import ServiceOutcome

from photition_api.docs.user.docs import (
    get_user_doc,
    login_doc,
    logout_doc,
    refresh_doc,
    registration_doc,
    update_user_doc,
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
from photition_api.services.user.reset_password_confirm import (
    ResetPasswordConfirmService,
)
from photition_api.services.user.reset_password_start import ResetPasswordStartService


class RegistrationView(APIView):
    permission_classes = (AllowAny,)

    @extend_schema(**registration_doc)
    def post(self, request, *args, **kwargs):
        outcome = ServiceOutcome(
            RegistrationService,
            request.data,
            {},
        )

        return Response(
            UserSerializer(outcome.result).data, status=outcome.response_status
        )


class LoginView(APIView):
    permission_classes = (AllowAny,)

    @extend_schema(**login_doc)
    def post(self, request, *args, **kwargs):
        outcome = ServiceOutcome(
            LoginService,
            request.data,
            {},
        )

        return Response(
            UserSerializer(outcome.result).data, status=outcome.response_status
        )


class LogoutView(APIView):
    permission_classes = (IsAuthenticated,)

    @extend_schema(**logout_doc)
    def post(self, request, *args, **kwargs):
        outcome = ServiceOutcome(LogoutService, {**kwargs, "user": request.user})

        return Response(None, status=outcome.response_status)


class RefreshView(APIView):
    permission_classes = (IsAuthenticated,)

    @extend_schema(**refresh_doc)
    def post(self, request, *args, **kwargs):
        outcome = ServiceOutcome(RefreshService, {**kwargs, "user": request.user})

        return Response(
            SessionTokenSerializer(outcome.result).data, status=outcome.response_status
        )


class CurrentView(APIView):
    permission_classes = (IsAuthenticated,)
    parser_classes = (MultiPartParser, FormParser)

    @extend_schema(**get_user_doc)
    def get(self, request, *args, **kwargs):
        outcome = ServiceOutcome(GetUserService, {"user": request.user})

        return Response(
            UserSerializer(outcome.result).data, status=outcome.response_status
        )

    @extend_schema(**update_user_doc)
    def patch(self, request, *args, **kwargs):
        outcome = ServiceOutcome(
            UpdateUserService,
            {"user": request.user, **request.data.dict()},
            request.FILES,
        )

        return Response(
            UserSerializer(outcome.result).data, status=outcome.response_status
        )


class ResetPasswordStartView(APIView):
    permission_classes = (AllowAny,)

    def post(self, request, *args, **kwargs):
        outcome = ServiceOutcome(
            ResetPasswordStartService,
            request.data,
        )

        return Response(None, status=outcome.response_status)


class ResetPasswordConfirmView(APIView):
    permission_classes = (AllowAny,)

    def post(self, request, *args, **kwargs):
        outcome = ServiceOutcome(
            ResetPasswordConfirmService,
            request.data,
        )

        return Response(None, status=outcome.response_status)
