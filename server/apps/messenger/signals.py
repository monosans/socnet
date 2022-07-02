from typing import Any

from django.db.models.signals import m2m_changed
from django.db.utils import IntegrityError
from django.dispatch import receiver
from django.utils.translation import gettext as _

from .models import Chat


@receiver(m2m_changed, sender=Chat.participants.through)
def verify_participants_count(
    instance: Chat, action: str, **kwargs: Any
) -> None:
    if action == "post_add" and instance.participants.count() != 2:
        raise IntegrityError(_("The chat must have 2 participants."))
