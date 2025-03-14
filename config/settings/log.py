from __future__ import annotations

LOG_CONFIG = {
    "version": 1,
    "disable_existing_loggers": False,
    "filters": {"require_admins": {"()": "socnet.core.log.RequireAdmins"}},
    "formatters": {
        "default": {
            "format": "%(asctime)s | %(levelname)-8s | %(name)s: %(message)s"
        },
        "access": {},
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
    "loggers": {
        "django.db.backends": {"level": "INFO"},
        "gunicorn.access": {
            "level": "INFO",
            "handlers": ["console", "mail_admins"],
        },
        "gunicorn.error": {
            "level": "INFO",
            "handlers": ["console", "mail_admins"],
        },
    },
}
