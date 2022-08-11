from __future__ import annotations

from typing import Any

from django.core.exceptions import ValidationError
from django.db.models.signals import m2m_changed
from django.dispatch import receiver
from django.utils.translation import gettext as _

from ..utils.pre_save_full_clean import pre_save_full_clean
from . import models
from .models import Chat

pre_save_full_clean(models.Chat)
pre_save_full_clean(models.Message)


@receiver(m2m_changed, sender=Chat.participants.through)
def validate_chat_participants_count(
    instance: Chat, action: str, **kwargs: Any
) -> None:
    if action == "post_add" and instance.participants.count() != 2:
        raise ValidationError(
            _("The chat must have 2 participants."),
            "invalid_chat_participants_count",
        )
