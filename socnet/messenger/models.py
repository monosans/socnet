from __future__ import annotations

from django.conf import settings
from django.db import models
from django.template import defaultfilters
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

from ..core.models import DateCreatedModel


class Chat(models.Model):
    members = models.ManyToManyField(
        to=settings.AUTH_USER_MODEL, related_name="chats", verbose_name=_("members")
    )

    class Meta:
        verbose_name = _("chat")
        verbose_name_plural = _("chats")

    def get_absolute_url(self) -> str:
        return reverse("messenger:chat", args=(self.pk,))


class Message(DateCreatedModel):
    sender = models.ForeignKey(
        to=settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="outgoing_messages",
        verbose_name=_("sender"),
    )
    chat = models.ForeignKey(
        to=Chat,
        on_delete=models.CASCADE,
        related_name="messages",
        verbose_name=_("chat"),
    )
    content = models.TextField(verbose_name=_("content"), max_length=4096)

    class Meta:
        verbose_name = _("message")
        verbose_name_plural = _("messages")

    @property
    def formatted_date_created(self) -> str:
        return defaultfilters.date(self.date_created, "Y-m-d H:i")
