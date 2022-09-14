from __future__ import annotations

from typing import Any, Set

from django.conf import settings
from django.core.exceptions import ValidationError
from django.db.models.signals import m2m_changed
from django.utils.translation import gettext as _

from .models import User as UserType


def forbid_self_subscription(
    instance: UserType, action: str, pk_set: Set[int], **kwargs: Any
) -> None:
    if action == "pre_add" and instance.pk in pk_set:
        raise ValidationError(
            _("You can't subscribe to yourself."), code="self_subscription"
        )


m2m_changed.connect(forbid_self_subscription, sender=settings.AUTH_USER_MODEL)
