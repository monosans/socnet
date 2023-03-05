from __future__ import annotations

from typing import Any

from django.db.models.signals import m2m_changed
from django.utils.translation import gettext as _

from . import exceptions, models

ALLOWED_MEMBERS_COUNT = 2


def validate_chat_members_count(
    instance: models.Chat, action: str, **kwargs: Any
) -> None:
    if action == "post_add" and instance.members.count() != ALLOWED_MEMBERS_COUNT:
        msg = _("The chat must have 2 members.")
        raise exceptions.ChatMembersCountError(msg)


m2m_changed.connect(validate_chat_members_count, sender=models.Chat.members.through)
