from typing import Any, Set

from django.contrib.auth import get_user_model
from django.db.models.signals import m2m_changed
from django.db.utils import IntegrityError
from django.dispatch import receiver
from django.utils.translation import gettext as _

from ..users.models import User as UserType

User = get_user_model()


@receiver(m2m_changed, sender=User.subscriptions.through)
def verify_self_subscription(
    instance: UserType, action: str, pk_set: Set[int], **kwargs: Any
) -> None:
    if action == "pre_add" and instance.pk in pk_set:
        raise IntegrityError(_("You can't subscribe to yourself."))
