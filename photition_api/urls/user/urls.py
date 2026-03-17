from django.urls import path

from photition_api.views.user.view import (
    CurrentView,
    LoginView,
    LogoutView,
    RefreshView,
    RegistrationView,
    ResetPasswordConfirmView,
    ResetPasswordStartView,
)

urlpatterns = [
    path("registration/", RegistrationView.as_view(), name="registration"),
    path("login/", LoginView.as_view(), name="login"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("refresh/", RefreshView.as_view(), name="refresh"),
    path("current/", CurrentView.as_view(), name="current"),
    path(
        "reset-password/", ResetPasswordStartView.as_view(), name="reset_password_start"
    ),
    path(
        "reset-password-confirm/",
        ResetPasswordConfirmView.as_view(),
        name="reset_password_confirm",
    ),
]
