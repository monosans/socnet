from __future__ import annotations

import logging
import smtplib
from typing import TYPE_CHECKING

from django.core import mail

from socnet.core.log import AdminEmailHandler

if TYPE_CHECKING:
    import pytest
    from pytest_django import Settings


def _record() -> logging.LogRecord:
    return logging.LogRecord("socnet", logging.ERROR, __file__, 1, "boom", None, None)


def test_admin_email_handler_mails_the_admins(settings: Settings) -> None:
    settings.ADMINS = ["admin@example.com"]

    AdminEmailHandler().handle(_record())

    assert len(mail.outbox) == 1
    assert mail.outbox[0].to == ["admin@example.com"]


def test_admin_email_handler_swallows_a_failed_send(
    settings: Settings, monkeypatch: pytest.MonkeyPatch
) -> None:
    settings.ADMINS = ["admin@example.com"]

    def fail(*_args: object, **_kwargs: object) -> None:
        msg = "connection refused"
        raise smtplib.SMTPException(msg)

    monkeypatch.setattr(mail, "mail_admins", fail)
    errors: list[logging.LogRecord] = []
    handler = AdminEmailHandler()
    monkeypatch.setattr(handler, "handleError", errors.append)

    handler.handle(_record())

    assert [record.getMessage() for record in errors] == ["boom"]
