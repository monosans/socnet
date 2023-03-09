from __future__ import annotations

from django.conf import settings
from django.db import models
from django.template import defaultfilters
from django.utils.translation import gettext_lazy as _

from ..core.models import DateCreatedModel, MarkdownContentModel


class Message(MarkdownContentModel, DateCreatedModel):
    sender = models.ForeignKey(
        to=settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="outgoing_messages",
        verbose_name=_("sender"),
    )
    recipient = models.ForeignKey(
        to=settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="incoming_messages",
        verbose_name=_("recipient"),
    )

    class Meta:
        verbose_name = _("message")
        verbose_name_plural = _("messages")

    @property
    def formatted_date_created(self) -> str:
        return defaultfilters.date(self.date_created, "Y-m-d H:i")
