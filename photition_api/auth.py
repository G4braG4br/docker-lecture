from django.utils import timezone
from rest_framework import exceptions
from rest_framework.authentication import BaseAuthentication

from photition_models.models import PhotitionSession, PhotitionUser


class SessionAuth(BaseAuthentication):
    def authenticate(self, request):
        token = request.headers.get("Session-Token")
        if not token:
            return None

        try:
            user_token = PhotitionSession.objects.get(session_token=token)
            user = PhotitionUser.objects.get(id=user_token.user_id)
            if user_token.expires_at < timezone.now():
                raise PhotitionSession.DoesNotExist
        except PhotitionSession.DoesNotExist:
            return None

        return user, None
