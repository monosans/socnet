from __future__ import annotations

import functools
import json
import logging
import secrets
from typing import TYPE_CHECKING, override

import pytest
import sentry_sdk
from django.test import Client
from django.urls import reverse
from sentry_sdk.transport import Transport

from config.settings.sentry import init_sentry
from socnet.blog import db_utils
from socnet.users.models import User
from tests.utils import auth_client

if TYPE_CHECKING:
    from collections.abc import Iterator
    from typing import NoReturn

    from django.http import HttpRequest
    from sentry_sdk.envelope import Envelope
    from sentry_sdk.types import Event


@pytest.fixture
def sentry_events(monkeypatch: pytest.MonkeyPatch) -> Iterator[list[Event]]:
    events: list[Event] = []

    class RecordingTransport(Transport):
        @override
        def capture_envelope(self, envelope: Envelope) -> None:
            if (event := envelope.get_event()) is not None:
                events.append(event)

    monkeypatch.setattr(
        sentry_sdk, "init", functools.partial(sentry_sdk.init, transport=RecordingTransport)
    )
    init_sentry("https://key@sentry.invalid/1")
    yield events
    sentry_sdk.get_client().close()
    sentry_sdk.get_global_scope().set_client(None)


# Django renders 500.html without a request, so the template sees no csrf_token.
@pytest.mark.ignore_template_errors
def test_server_error_event_leaks_no_secrets(
    sentry_events: list[Event], monkeypatch: pytest.MonkeyPatch
) -> None:
    def fail(request: HttpRequest, *_args: object) -> NoReturn:
        password = request.POST["password"]
        User.objects.filter(password=password).exists()
        raise RuntimeError

    monkeypatch.setattr(db_utils, "get_posts_preview_qs", fail)
    # Random, so the source lines sent with the event can't contain it.
    secret = secrets.token_urlsafe()
    client = Client(raise_request_exception=False)
    auth_client(client)
    client.post(reverse("blog:posts"), {"password": secret})

    [event] = sentry_events
    assert event["exception"]["values"][-1]["type"] == "RuntimeError"
    frame = event["exception"]["values"][-1]["stacktrace"]["frames"][-1]
    assert "password" in frame["vars"]
    assert secret not in json.dumps(event)
    assert not event.get("user")


def test_logged_error_becomes_event_without_access_log(sentry_events: list[Event]) -> None:
    logging.getLogger("granian.access").info("GET / 200")
    logging.getLogger("socnet").error("boom")

    [event] = sentry_events
    assert event["logentry"]["message"] == "boom"
    assert "granian.access" not in json.dumps(event.get("breadcrumbs"))
