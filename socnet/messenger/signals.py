from __future__ import annotations

from typing import Any

from django.core.exceptions import ValidationError
from django.db.models.signals import m2m_changed
from django.utils.translation import gettext as _

from . import models


def validate_chat_participants_count(
    instance: models.Chat, action: str, **kwargs: Any
) -> None:
    if action == "post_add" and instance.participants.count() != 2:
        raise ValidationError(
            _("The chat must have 2 participants."),
            code="invalid_chat_participants_count",
        )


m2m_changed.connect(
    validate_chat_participants_count, sender=models.Chat.participants.through
)
