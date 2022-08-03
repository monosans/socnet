"""https://docs.djangoproject.com/en/4.1/ref/settings/"""
from __future__ import annotations

from pathlib import Path
from typing import Any

import environ
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
    "channels",
    "crispy_forms",
    "crispy_bootstrap5",
    "logentry_admin",
    "rest_framework",
    "socnet.main",
    "socnet.messenger",
    "socnet.users",
    "django_cleanup",
]

AUTHENTICATION_BACKENDS = [
    "django.contrib.auth.backends.ModelBackend",
    "allauth.account.auth_backends.AuthenticationBackend",
]
AUTH_USER_MODEL = "users.User"
LOGIN_REDIRECT_URL = "index"
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

_PASS = "django.contrib.auth.password_validation"
AUTH_PASSWORD_VALIDATORS = [
    {"NAME": f"{_PASS}.UserAttributeSimilarityValidator"},
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
SECURE_BROWSER_XSS_FILTER = True
X_FRAME_OPTIONS = "DENY"

EMAIL_TIMEOUT = 5

ACCOUNT_AUTHENTICATION_METHOD = "username_email"
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_EMAIL_VERIFICATION = "mandatory"
ACCOUNT_PRESERVE_USERNAME_CASING = False

REST_FRAMEWORK = {
    "DEFAULT_PERMISSION_CLASSES": [
        "socnet.api.permissions.DjangoModelPermissionsWithViewPermissionCheck"
    ],
    "DEFAULT_PAGINATION_CLASS": (
        "rest_framework.pagination.LimitOffsetPagination"
    ),
    "DEFAULT_FILTER_BACKENDS": [
        "rest_framework.filters.SearchFilter",
        "rest_framework.filters.OrderingFilter",
    ],
    "PAGE_SIZE": 10,
}

CHANNEL_LAYERS: dict[str, dict[str, Any]] = {
    "default": {"BACKEND": "channels.layers.InMemoryChannelLayer"}
}
