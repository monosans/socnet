from __future__ import annotations

from typing import Any, Set

from django.db.models.signals import m2m_changed
from django.utils.translation import gettext as _

from . import exceptions
from .models import User


def forbid_self_subscription(
    instance: User, action: str, pk_set: Set[int], **kwargs: Any
) -> None:
    if action == "pre_add" and instance.pk in pk_set:
        raise exceptions.SelfSubscriptionError(
            _("You can't subscribe to yourself.")
        )


m2m_changed.connect(
    forbid_self_subscription, sender=User.subscriptions.through
)
