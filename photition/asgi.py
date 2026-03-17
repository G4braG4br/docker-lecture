import os

from django.core.asgi import get_asgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "photition.settings.production")
django_asgi_app = get_asgi_application()


def get_websocket_app():
    from channels.auth import AuthMiddlewareStack
    from channels.routing import ProtocolTypeRouter, URLRouter

    from photition_notice.middlewares import QueryAuthMiddleware
    from photition_notice.routing import notice_urlpatterns

    return ProtocolTypeRouter(
        {
            "http": django_asgi_app,
            "websocket": QueryAuthMiddleware(URLRouter(notice_urlpatterns)),
        }
    )


application = get_websocket_app()
