from __future__ import annotations

from typing import Any

from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.db.models.signals import m2m_changed
from django.dispatch import receiver
from django.utils.translation import gettext as _

from ..users.models import User as UserType
from ..utils.pre_save_full_clean import pre_save_full_clean

User: type[UserType] = get_user_model()

pre_save_full_clean(User)


@receiver(m2m_changed, sender=User.subscriptions.through)
def forbid_self_subscription(
    instance: UserType, action: str, pk_set: set[int], **kwargs: Any
) -> None:
    if action == "pre_add" and instance.pk in pk_set:
        raise ValidationError(
            _("You can't subscribe to yourself."), "self_subscription"
        )
