from debug_toolbar.toolbar import debug_toolbar_urls
from decouple import config
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from django.views.static import serve
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView
from oauth2_provider import urls as oauth2_urls

from photition.settings import django

IS_DEBUG = config("IS_DEBUG", cast=bool)

urlpatterns = [
    path("o/", include("oauth2_provider.urls", namespace="oauth2_provider")),
    path("admin/", admin.site.urls),
    path("auth/", include("social_django.urls", namespace="social")),
    path("auth/", include("drf_social_oauth2.urls", namespace="drf_social_oauth2")),
    path("api/", include("photition_api.urls.user.urls")),
    path("api/", include("photition_api.urls.photo.urls")),
    path("api/", include("photition_api.urls.notice.urls")),
    path("api/schema/", SpectacularAPIView.as_view(), name="schema"),
    path(
        "api/schema/swagger-ui/",
        SpectacularSwaggerView.as_view(url_name="schema"),
        name="swagger-ui",
    ),
]

if not IS_DEBUG:
    urlpatterns += [
        path("media/<path:path>", serve, {"document_root": settings.MEDIA_ROOT}),
    ]
else:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += [path("silk/", include("silk.urls", namespace="silk"))]

urlpatterns += debug_toolbar_urls()
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
