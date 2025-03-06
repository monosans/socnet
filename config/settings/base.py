# ruff: noqa: E402
from __future__ import annotations

import logging

if not logging.root.handlers:
    import logging.config

    from config.settings.log import LOG_CONFIG as _LOG_CONFIG

    logging.config.dictConfig(_LOG_CONFIG)
    logging.getLogger(__name__).warning("Configured logging")

import os
from pathlib import Path
from typing import TYPE_CHECKING

import django_stubs_ext as _django_stubs_ext
import environ
from django.contrib.messages import constants as messages
from django.utils.translation import gettext_lazy as _

if TYPE_CHECKING:
    from typing import Any

_django_stubs_ext.monkeypatch(include_builtins=False)

BASE_DIR = Path().resolve(strict=True)

env = environ.Env()
env.smart_cast = False

# Needed for running mypy outside of docker
if "DJANGO_SECRET_KEY" not in os.environ:  # pragma: no cover
    env.read_env(str(BASE_DIR / ".env"))
    logging.getLogger(__name__).warning("Read .env")

APPS_DIR = BASE_DIR / "socnet"

DEBUG = False
SECRET_KEY = env.str("DJANGO_SECRET_KEY")

TIME_ZONE = "UTC"
LANGUAGE_CODE = "en-us"
USE_I18N = True
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
        "OPTIONS": {"pool": True},
    }
}

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

ROOT_URLCONF = "config.urls"
ASGI_APPLICATION = "config.asgi.application"

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
    "allauth.mfa",
    "django_bootstrap5",
    "django_filters",
    "django_htmx",
    "logentry_admin",
    "socnet.allauth",
    "socnet.api",
    "socnet.core",
    "socnet.blog",
    "socnet.messenger",
    "socnet.users",
    "django_cleanup.apps.CleanupConfig",
]

ADMIN_URL = env.str("ADMIN_URL").strip("/")
AUTHENTICATION_BACKENDS = [
    "django.contrib.auth.backends.ModelBackend",
    "allauth.account.auth_backends.AuthenticationBackend",
]
AUTH_USER_MODEL = "users.User"
LOGIN_REDIRECT_URL = "core:index"
LOGIN_URL = "account_login"
LOGOUT_REDIRECT_URL = LOGIN_URL

# https://docs.djangoproject.com/en/5.1/topics/auth/passwords/#using-argon2-with-django
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
    "django_htmx.middleware.HtmxMiddleware",
    "django.middleware.locale.LocaleMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "allauth.account.middleware.AccountMiddleware",
    "socnet.core.middleware.MinifyHtmlMiddleware",
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
ACCOUNT_ADAPTER = "socnet.allauth.adapter.AccountAdapter"
ACCOUNT_FORMS = {
    "add_email": "socnet.allauth.forms.AddEmailForm",
    "login": "socnet.allauth.forms.LoginForm",
    "reset_password": "socnet.allauth.forms.ResetPasswordForm",
    "signup": "socnet.allauth.forms.SignupForm",
}

CHANNEL_LAYERS: dict[str, dict[str, Any]] = {
    "default": {"BACKEND": "channels.layers.InMemoryChannelLayer"}
}
