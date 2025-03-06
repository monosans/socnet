from __future__ import annotations

import socket

from config.settings.base import *

DEBUG = True

EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"

INSTALLED_APPS += ["debug_toolbar", "extra_checks"]
MIDDLEWARE += ["debug_toolbar.middleware.DebugToolbarMiddleware"]

TEMPLATES[0]["OPTIONS"]["string_if_invalid"] = (  # type: ignore[index]
    "INVALID EXPRESSION: %s"
)

# https://django-debug-toolbar.readthedocs.io/en/latest/installation.html#configure-internal-ips
INTERNAL_IPS = [
    ip[: ip.rfind(".")] + ".1"
    for ip in socket.gethostbyname_ex(socket.gethostname())[2]
] + ["127.0.0.1", "10.0.2.2"]

DEBUG_TOOLBAR_CONFIG = {
    "DISABLE_PANELS": {
        "debug_toolbar.panels.history.HistoryPanel",
        "debug_toolbar.panels.versions.VersionsPanel",
        "debug_toolbar.panels.settings.SettingsPanel",
        "debug_toolbar.panels.headers.HeadersPanel",
        "debug_toolbar.panels.request.RequestPanel",
        "debug_toolbar.panels.staticfiles.StaticFilesPanel",
        "debug_toolbar.panels.templates.TemplatesPanel",
        "debug_toolbar.panels.cache.CachePanel",
        "debug_toolbar.panels.signals.SignalsPanel",
        "debug_toolbar.panels.redirects.RedirectsPanel",
        "debug_toolbar.panels.profiling.ProfilingPanel",
    },
    "ENABLE_STACKTRACES": False,
}

MEDIA_ROOT = str(APPS_DIR / "media")

EXTRA_CHECKS = {
    "checks": [
        "no-unique-together",
        "model-admin",
        "field-file-upload-to",
        "field-verbose-name",
        "field-verbose-name-gettext",
        "field-verbose-name-gettext-case",
        "field-help-text-gettext",
        "field-text-null",
        "field-null",
        "field-foreign-key-db-index",
        "field-related-name",
        "field-default-null",
        "field-choices-constraint",
    ]
}


if _SENTRY_DSN := env.str("SENTRY_DSN", None):
    import sentry_sdk

    sentry_sdk.init(dsn=_SENTRY_DSN, environment="local")
