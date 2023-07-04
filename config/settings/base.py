# https://docs.djangoproject.com/en/4.2/ref/settings/
from __future__ import annotations

import logging
from pathlib import Path

current_file = Path(__file__).resolve(strict=True)

# Set up logging only if it has not already been set up by uvicorn or gunicorn
if not logging.root.handlers:
    import json
    import logging.config

    logging.config.dictConfig(
        json.loads(current_file.with_name("logging.json").read_bytes())
    )

from typing import Any, Dict  # noqa: E402

import environ  # noqa: E402
from django.contrib.messages import constants as messages  # noqa: E402
from django.utils.translation import gettext_lazy as _  # noqa: E402

BASE_DIR = current_file.parents[2]

env = environ.Env()
env.smart_cast = False

# Needed for running mypy outside of docker
if env.bool("READ_ENV_EXAMPLE", default=True):  # pragma: no cover
    env.read_env(str(BASE_DIR / ".env.example"))

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
        "HOST": env.str("POSTGRES_HOST"),
        "PORT": env.int("POSTGRES_PORT"),
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
    "allauth.socialaccount",
    "django_otp",
    "django_otp.plugins.otp_totp",
    "django_otp.plugins.otp_static",
    "allauth_2fa",
    "django_bootstrap5",
    "django_filters",
    "drf_spectacular",
    "logentry_admin",
    "rest_framework",
    "socnet.allauth",
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

# https://docs.djangoproject.com/en/4.2/topics/auth/passwords/#using-argon2-with-django
PASSWORD_HASHERS = [
    "django.contrib.auth.hashers.Argon2PasswordHasher",
    "django.contrib.auth.hashers.PBKDF2PasswordHasher",
    "django.contrib.auth.hashers.PBKDF2SHA1PasswordHasher",
    "django.contrib.auth.hashers.BCryptSHA256PasswordHasher",
    "django.contrib.auth.hashers.ScryptPasswordHasher",
]

AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {
        "NAME": (
            "django.contrib.auth.password_validation.NumericPasswordValidator"
        )
    },
]

MIDDLEWARE = [
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.locale.LocaleMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django_otp.middleware.OTPMiddleware",
    "djangorestframework_camel_case.middleware.CamelCaseMiddleWare",
    "socnet.core.middleware.ResponseHeadersMiddleware",
]

STATIC_URL = "static/"
STATICFILES_DIRS = [str(APPS_DIR / "static" / "public")]

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

SESSION_COOKIE_HTTPONLY = True
CSRF_COOKIE_HTTPONLY = True

EMAIL_TIMEOUT = 5

LOGGING_CONFIG: None = None

MESSAGE_TAGS = {messages.DEBUG: "", messages.ERROR: "danger"}

ACCOUNT_AUTHENTICATION_METHOD = "username_email"
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_EMAIL_VERIFICATION = "mandatory"
ACCOUNT_ADAPTER = "socnet.allauth.adapter.AuthAdapter"

REST_FRAMEWORK = {
    "DEFAULT_RENDERER_CLASSES": [
        "djangorestframework_camel_case.render.CamelCaseJSONRenderer"
    ],
    "DEFAULT_PARSER_CLASSES": [
        "djangorestframework_camel_case.parser.CamelCaseJSONParser",
        "djangorestframework_camel_case.parser.CamelCaseFormParser",
        "djangorestframework_camel_case.parser.CamelCaseMultiPartParser",
    ],
    "DEFAULT_PERMISSION_CLASSES": [
        "socnet.api.permissions.ActualDjangoModelPermissions"
    ],
    "DEFAULT_SCHEMA_CLASS": "drf_spectacular.openapi.AutoSchema",
    "DEFAULT_FILTER_BACKENDS": [
        "django_filters.rest_framework.DjangoFilterBackend",
        "rest_framework.filters.OrderingFilter",
    ],
    "DEFAULT_PAGINATION_CLASS": (
        "rest_framework.pagination.LimitOffsetPagination"
    ),
    "PAGE_SIZE": 10,
}
SPECTACULAR_SETTINGS = {
    "SERVE_PERMISSIONS": ["rest_framework.permissions.IsAdminUser"],
    "POSTPROCESSING_HOOKS": [
        "drf_spectacular.hooks.postprocess_schema_enums",
        "drf_spectacular.contrib.djangorestframework_camel_case.camelize_serializer_fields",
    ],
    "CAMELIZE_NAMES": True,
    "TITLE": "SocNet API",
}

CHANNEL_LAYERS: Dict[str, Dict[str, Any]] = {
    "default": {"BACKEND": "channels.layers.InMemoryChannelLayer"}
}

OTP_ADMIN_HIDE_SENSITIVE_DATA = True
