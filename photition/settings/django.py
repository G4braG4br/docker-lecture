import os
from pathlib import Path

from corsheaders.defaults import default_headers
from decouple import config

from .database import *
from .restframework import *

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

config.encoding = "cp1251"

SECRET_KEY = config("SECRET_KEY")
GOOGLE_CLIENT_ID = config("GOOGLE_CLIENT_ID")
GOOGLE_CLIENT_SECRET = config("GOOGLE_CLIENT_SECRET")
VK_CLIENT_ID = config("VK_CLIENT_ID")
VK_CLIENT_SECRET = config("VK_CLIENT_SECRET")
REDIS_HOST = config("REDIS_HOST")
REDIS_PORT = int(config("REDIS_PORT"))
IS_DEBUG = config("IS_DEBUG", cast=bool)
REDIS_PASSWORD = config("REDIS_PASSWORD", "")
EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = config("EMAIL_HOST", "test@test.com")
EMAIL_PORT = config("EMAIL_PORT", "20")
EMAIL_HOST_USER = config("EMAIL_HOST_USER", "test")
EMAIL_HOST_PASSWORD = config("EMAIL_HOST_PASSWORD", "test")
EMAIL_USE_TLS = config("EMAIL_USE_TLS", False)
DOMAIN = config("DOMAIN", "localhost:8000")
SCHEMA = config("SCHEMA", "http")
BASE_URL = f"{SCHEMA}://{DOMAIN}"

DEBUG = IS_DEBUG

ALLOWED_HOSTS = ["*", ".railway.app"]

ASGI_APPLICATION = "photition.asgi.application"

INSTALLED_APPS = [
    "daphne",
    "whitenoise.runserver_nostatic",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.sites",
    "photition_models.apps.PhotitionModelsConfig",
    "photition_notice.apps.PhotitionNoticeConfig",
    "rest_framework",
    "imagekit",
    "drf_spectacular",
    "drf_spectacular_sidecar",
    "channels",
    "oauth2_provider",
    "social_django",
    "drf_social_oauth2",
    "corsheaders",
    "service_objects",
    "django_fsm",
    "debug_toolbar",
    "django_materialized_view",
    "photition_api.apps.PhotitionApiConfig",
    "django_celery_beat",
    "silk",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "debug_toolbar.middleware.DebugToolbarMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.locale.LocaleMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "silk.middleware.SilkyMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

INTERNAL_IPS = [
    "127.0.0.1",
]

SITE_ID = 1

AUTH_USER_MODEL = "photition_models.PhotitionUser"

ROOT_URLCONF = "photition.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [os.path.join(BASE_DIR, "templates")],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                "social_django.context_processors.backends",
                "social_django.context_processors.login_redirect",
            ],
        },
    },
]

AUTHENTICATION_BACKENDS = (
    "social_core.backends.google.GoogleOAuth2",
    "social_core.backends.vk.VKOAuth2",
    "drf_social_oauth2.backends.DjangoOAuth2",
    "django.contrib.auth.backends.ModelBackend",
)

SOCIAL_AUTH_GOOGLE_OAUTH2_KEY = GOOGLE_CLIENT_ID
SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET = GOOGLE_CLIENT_SECRET

SOCIAL_AUTH_GOOGLE_OAUTH2_SCOPE = [
    "https://www.googleapis.com/auth/userinfo.email",
    "https://www.googleapis.com/auth/userinfo.profile",
]

SOCIAL_AUTH_VK_OAUTH2_KEY = VK_CLIENT_ID
SOCIAL_AUTH_VK_OAUTH2_SECRET = VK_CLIENT_SECRET

SOCIAL_AUTH_VK_OAUTH2_SCOPE = ["email"]

SOCIAL_AUTH_GOOGLE_OAUTH2_WHITELISTED_DOMAINS = ["127.0.0.1"]

SOCIAL_AUTH_REDIRECT_IS_HTTPS = False

SOCIAL_AUTH_GOOGLE_OAUTH2_WHITELISTED_DOMAINS = []
SOCIAL_AUTH_GOOGLE_OAUTH2_WHITELISTED_EMAILS = []

SOCIAL_AUTH_PIPELINE = (
    "social_core.pipeline.social_auth.social_details",
    "social_core.pipeline.social_auth.social_uid",
    "social_core.pipeline.social_auth.auth_allowed",
    "social_core.pipeline.social_auth.social_user",
    "social_core.pipeline.social_auth.associate_user",
    "social_core.pipeline.social_auth.load_extra_data",
    "social_core.pipeline.user.user_details",
    "photition_api.pipelines.redirect_frontend",
)

STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR / "staticfiles"
STATICFILES_DIRS = []

if not DEBUG:
    STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

MEDIA_URL = "/media/"
if IS_DEBUG:
    MEDIA_ROOT = BASE_DIR / "media"
else:
    MEDIA_ROOT = "/media/"
CORS_ALLOW_ALL_ORIGINS = True

CORS_ALLOW_HEADERS = list(default_headers) + ["Session-Token"]

CORS_ALLOW_CREDENTIALS = True

CSRF_TRUSTED_ORIGINS = [
    "https://photition-api-production.up.railway.app",
    "https://*.railway.app",
    "http://127.0.0.1",
]

CSRF_COOKIE_SECURE = True
CSRF_COOKIE_HTTPONLY = False
CSRF_COOKIE_SAMESITE = "Lax"

SESSION_COOKIE_SECURE = True
SESSION_COOKIE_SAMESITE = "Lax"

WSGI_APPLICATION = "photition.wsgi.application"

CELERY_BROKER_URL = f"redis://:{REDIS_PASSWORD}@{REDIS_HOST}:{REDIS_PORT}"
CELERY_BEAT_SCHEDULER = "django_celery_beat.schedulers:DatabaseScheduler"

CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "channels_redis.core.RedisChannelLayer",
        "CONFIG": {
            "hosts": [
                {
                    "host": REDIS_HOST,
                    "port": REDIS_PORT,
                    "password": REDIS_PASSWORD,
                }
            ],
        },
    },
}

CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": f"redis://{REDIS_HOST}:{REDIS_PORT}/2",
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        },
    }
}

SESSION_TOKEN_EXPIRES = int(config("SESSION_TOKEN_EXPIRES", 3600))
