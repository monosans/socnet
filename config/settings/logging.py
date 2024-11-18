from __future__ import annotations

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "filters": {"require_admins": {"()": "socnet.core.log.RequireAdmins"}},
    "formatters": {
        "default": {
            "format": "%(asctime)s | %(levelname)-8s | %(name)s: %(message)s"
        }
    },
    "handlers": {
        "console": {
            "level": "NOTSET",
            "class": "logging.StreamHandler",
            "formatter": "default",
        },
        "mail_admins": {
            "level": "ERROR",
            "filters": ["require_admins"],
            "class": "django.utils.log.AdminEmailHandler",
            "reporter_class": "django.views.debug.ExceptionReporter",
        },
    },
    "root": {"level": "INFO", "handlers": ["console", "mail_admins"]},
    "loggers": {"_granian": {}},
}
