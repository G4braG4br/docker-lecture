from decouple import config
from django.shortcuts import redirect
from service_objects.services import ServiceOutcome

from photition_api.services.user.oauth_user import OAuthUserService

CLIENT = config("CLIENT_HOST", "test")


def redirect_frontend(backend, user, response, *args, **kwargs):
    if backend.name == "google-oauth2":
        password = response["access_token"]
        username = response["name"]
        email = response["email"]
        picture = response.get("picture")

        outcome = ServiceOutcome(
            OAuthUserService,
            {
                "email": email,
                "username": username,
                "password": password,
                "avatar": picture,
            },
        )
        token = outcome.result

        return redirect(f"{CLIENT}social/?token={token}")
    return None
