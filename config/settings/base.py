"""https://docs.djangoproject.com/en/4.1/ref/settings/"""
from __future__ import annotations

from pathlib import Path
from typing import Any, Dict

import environ
from django.contrib.messages import constants as messages
from django.utils.translation import gettext_lazy as _

BASE_DIR = Path(__file__).resolve(strict=True).parent.parent.parent

env = environ.Env()
env.smart_cast = False

# Needed for running mypy outside of docker
if env.bool("READ_ENV_TEMPLATE", default=True):  # pragma: no cover
    env.read_env(str(BASE_DIR / ".env.template"))

APPS_DIR = BASE_DIR / "socnet"

DEBUG = False
SECRET_KEY = env.str("DJANGO_SECRET_KEY")

TIME_ZONE = "UTC"
LANGUAGE_CODE = "en-us"
USE_I18N = True
USE_L10N = True
USE_TZ = True
LANGUAGES = [("en", _("English")), ("ru", _("Russian"))]
LOCALE_PATHS = [str(BASE_DIR / "locale")]

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": env.str("POSTGRES_DB"),
        "USER": env.str("POSTGRES_USER"),
        "PASSWORD": env.str("POSTGRES_PASSWORD"),
        "HOST": "postgres",
        "PORT": 5432,
        "ATOMIC_REQUESTS": True,
    }
}

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

ROOT_URLCONF = "config.urls"
ASGI_APPLICATION = "config.asgi.application"
WSGI_APPLICATION = "config.wsgi.application"

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.admindocs",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.postgres",
    "allauth",
    "allauth.account",
    "django_otp",
    "django_otp.plugins.otp_totp",
    "django_otp.plugins.otp_static",
    "allauth_2fa",
    "crispy_forms",
    "crispy_bootstrap5",
    "django_filters",
    "drf_spectacular",
    "logentry_admin",
    "rest_framework",
    "socnet.api",
    "socnet.core",
    "socnet.blog",
    "socnet.messenger",
    "socnet.users",
    "django_cleanup.apps.CleanupConfig",
]

AUTHENTICATION_BACKENDS = [
    "django.contrib.auth.backends.ModelBackend",
    "allauth.account.auth_backends.AuthenticationBackend",
]
AUTH_USER_MODEL = "users.User"
LOGIN_REDIRECT_URL = "core:index"
LOGIN_URL = "account_login"
LOGOUT_REDIRECT_URL = LOGIN_URL

# https://docs.djangoproject.com/en/4.1/topics/auth/passwords/#using-argon2-with-django
PASSWORD_HASHERS = [
    "django.contrib.auth.hashers.Argon2PasswordHasher",
    "django.contrib.auth.hashers.PBKDF2PasswordHasher",
    "django.contrib.auth.hashers.PBKDF2SHA1PasswordHasher",
    "django.contrib.auth.hashers.BCryptSHA256PasswordHasher",
    "django.contrib.auth.hashers.ScryptPasswordHasher",
]

_PASS = "django.contrib.auth.password_validation"  # noqa: S105
AUTH_PASSWORD_VALIDATORS = [
    {"NAME": f"{_PASS}.MinimumLengthValidator"},
    {"NAME": f"{_PASS}.CommonPasswordValidator"},
    {"NAME": f"{_PASS}.NumericPasswordValidator"},
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.locale.LocaleMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "django_otp.middleware.OTPMiddleware",
]

STATIC_URL = "static/"
STATICFILES_DIRS = [str(APPS_DIR / "static")]

MEDIA_URL = "media/"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [str(APPS_DIR / "templates")],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ]
        },
    }
]

CRISPY_TEMPLATE_PACK = "bootstrap5"
CRISPY_ALLOWED_TEMPLATE_PACKS = "bootstrap5"

SESSION_COOKIE_HTTPONLY = True
CSRF_COOKIE_HTTPONLY = True
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = "DENY"

EMAIL_TIMEOUT = 5

ADMINS = [(env.str("ADMIN_NAME"), env.str("ADMIN_EMAIL"))]
MANAGERS = ADMINS

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "verbose": {
            "format": (
                "%(levelname)s %(asctime)s %(module)s "
                "%(process)d %(thread)d %(message)s"
            )
        }
    },
    "handlers": {
        "console": {
            "level": "DEBUG",
            "class": "logging.StreamHandler",
            "formatter": "verbose",
        }
    },
    "root": {"level": "INFO", "handlers": ["console"]},
}

MESSAGE_TAGS = {messages.DEBUG: "", messages.ERROR: "danger"}

ACCOUNT_AUTHENTICATION_METHOD = "username_email"
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_EMAIL_VERIFICATION = "mandatory"
ACCOUNT_ADAPTER = "allauth_2fa.adapter.OTPAdapter"

REST_FRAMEWORK = {
    "DEFAULT_RENDERER_CLASSES": ["rest_framework.renderers.JSONRenderer"],
    "DEFAULT_PERMISSION_CLASSES": [
        "socnet.api.permissions.ActualDjangoModelPermissions"
    ],
    "DEFAULT_SCHEMA_CLASS": "drf_spectacular.openapi.AutoSchema",
    "DEFAULT_FILTER_BACKENDS": [
        "django_filters.rest_framework.DjangoFilterBackend",
        "rest_framework.filters.OrderingFilter",
    ],
    "DEFAULT_PAGINATION_CLASS": "rest_framework.pagination.LimitOffsetPagination",
    "PAGE_SIZE": 10,
}
SPECTACULAR_SETTINGS = {"SERVE_PERMISSIONS": ["rest_framework.permissions.IsAdminUser"]}

CHANNEL_LAYERS: Dict[str, Dict[str, Any]] = {
    "default": {"BACKEND": "channels.layers.InMemoryChannelLayer"}
}
