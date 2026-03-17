from urllib.parse import parse_qs

from channels.db import database_sync_to_async
from django.contrib.auth.models import AnonymousUser
from django.utils import timezone

from photition_models.models.user.photition_session_model import PhotitionSession
from photition_models.models.user.photition_user_model import PhotitionUser


@database_sync_to_async
def get_user(token):
    try:
        user_token = PhotitionSession.objects.get(session_token=token)
        user = PhotitionUser.objects.get(id=user_token.user_id)
        if user_token.expires_at < timezone.now():
            raise PhotitionSession.DoesNotExist
        return user
    except PhotitionUser.DoesNotExist:
        return AnonymousUser()


class QueryAuthMiddleware:

    def __init__(self, app):
        self.app = app

    async def __call__(self, scope, receive, send):
        query_string = parse_qs(scope["query_string"].decode())
        token = query_string.get("token", [None])[0]
        scope["user"] = await get_user(token)

        return await self.app(scope, receive, send)
