from __future__ import annotations

from django.conf import settings
from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

from ..users.models import User as UserType


class Chat(models.Model):
    participants = models.ManyToManyField(
        to=settings.AUTH_USER_MODEL,
        related_name="chats",
        verbose_name=_("participants"),
    )

    class Meta:
        verbose_name = _("chat")
        verbose_name_plural = _("chats")

    def get_absolute_url(self) -> str:
        return reverse("chat", args=(self.pk,))

    def get_companion(self, user: UserType) -> UserType:
        return next(
            filter(
                lambda participant: participant != user,
                self.participants.all(),
            )
        )


class Message(models.Model):
    user = models.ForeignKey(
        to=settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="outgoing_messages",
        verbose_name=_("user"),
    )
    chat = models.ForeignKey(
        to=Chat,
        on_delete=models.CASCADE,
        related_name="messages",
        verbose_name=_("chat"),
    )
    text = models.TextField(verbose_name=_("text"), max_length=4096)
    date = models.DateTimeField(verbose_name=_("date/time"), auto_now_add=True)

    class Meta:
        verbose_name = _("message")
        verbose_name_plural = _("messages")

    @property
    def simple_date(self) -> str:
        return self.date.strftime("%Y-%m-%d %H:%M")
