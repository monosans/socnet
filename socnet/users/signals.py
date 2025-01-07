from __future__ import annotations

from typing import TYPE_CHECKING

from django.db.models.signals import m2m_changed
from django.utils.translation import gettext as _

from socnet.users import exceptions
from socnet.users.models import User

if TYPE_CHECKING:
    from typing import Any


def forbid_self_subscription(
    instance: User, action: str, pk_set: set[int], **_kwargs: Any
) -> None:
    if action == "pre_add" and instance.pk in pk_set:
        msg = _("You can't subscribe to yourself.")
        raise exceptions.SelfSubscriptionError(msg)


m2m_changed.connect(forbid_self_subscription, sender=User.subscriptions.through)
