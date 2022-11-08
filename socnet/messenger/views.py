from __future__ import annotations

from time import mktime

from django.contrib.auth.decorators import login_required
from django.db.models import Prefetch
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST, require_safe

from ..users.models import User
from ..users.types import AuthedRequest
from . import forms, models


@require_POST
@login_required
def chat_get_or_create_view(request: AuthedRequest, pk: int) -> HttpResponse:
    chat, created = models.Chat.objects.filter(
        participants__in=[request.user.pk]
    ).get_or_create(participants__in=[pk])
    if created:
        chat.participants.set([request.user.pk, pk])
    return redirect(chat)


@require_safe
@login_required
def chat_view(request: AuthedRequest, pk: int) -> HttpResponse:
    prefetch = Prefetch(
        "messages",
        models.Message.objects.select_related("user")
        .order_by("pk")
        .only("chat_id", "date", "text", "user__image", "user__username"),
    )
    qs = request.user.chats.filter(pk=pk).prefetch_related(prefetch).only("pk")
    chat = get_object_or_404(qs)
    form = forms.MessageCreationForm()
    context = {"chat": chat, "form": form}
    return render(request, "messenger/chat.html", context)


@require_safe
@login_required
def chats_view(request: AuthedRequest) -> HttpResponse:
    def chat_sort_key(chat: models.Chat) -> float:
        message = chat.messages.first()
        if not message:
            return float("-inf")
        return mktime(message.date.timetuple())

    prefetches = (
        Prefetch(
            "messages",
            models.Message.objects.order_by("chat_id", "-pk")
            .distinct("chat_id")
            .only("chat_id", "date", "text"),
        ),
        Prefetch(
            "participants",
            User.objects.exclude(pk=request.user.pk).only(
                "display_name", "image", "username"
            ),
        ),
    )
    chats = request.user.chats.prefetch_related(*prefetches)
    context = {"chats": sorted(chats, key=chat_sort_key, reverse=True)}
    return render(request, "messenger/chats.html", context)
