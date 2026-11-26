from __future__ import annotations

import logging

import sentry_sdk
from sentry_sdk.integrations.asyncio import AsyncioIntegration
from sentry_sdk.integrations.logging import LoggingIntegration, ignore_logger_for_events


def init_sentry(dsn: str, environment: str | None = None) -> None:
    sentry_sdk.init(
        dsn=dsn,
        environment=environment,
        integrations=(
            AsyncioIntegration(),
            # Errors that are only logged, like the chat consumer's, become events.
            # Sentry Logs stay off: the container log already keeps every line.
            LoggingIntegration(level=None, event_level=logging.ERROR),
        ),
        data_collection={
            # Request bodies go out unfiltered, passwords and messages included.
            "http_bodies": [],
            # SQL and Redis arguments carry session keys and message texts.
            "database_query_data": False,
            # Masks locals whose names look secret (password, token, key...).
            "stack_frame_variables": {"mode": "denylist"},
        },
    )
    # Granian logs each request after its scope is gone, so the access lines
    # would pile up as breadcrumbs on other users' events.
    ignore_logger_for_events("granian.access")
