from __future__ import annotations

from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.db.models import Prefetch
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST, require_safe

from ..users.types import AuthedRequest
from . import forms, models

User = get_user_model()


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
        models.Message.objects.select_related("user").only(
            "text", "date", "chat_id", "user__username", "user__image"
        ),
    )
    qs = request.user.chats.prefetch_related(prefetch).only("pk")
    chat = get_object_or_404(qs, pk=pk)
    form = forms.MessageCreationForm()
    context = {"chat": chat, "form": form}
    return render(request, "messenger/chat.html", context)


@require_safe
@login_required
def chats_view(request: AuthedRequest) -> HttpResponse:
    prefetches = (
        Prefetch(
            "participants",
            User.objects.only("username", "image", "first_name", "last_name"),
        ),
        Prefetch(
            "messages",
            models.Message.objects.order_by("chat_id", "-pk")
            .distinct("chat_id")
            .only("text", "date", "chat_id"),
        ),
    )
    chats = request.user.chats.prefetch_related(*prefetches)
    chats_with_companion = (
        (chat, chat.get_companion(request.user)) for chat in chats
    )
    context = {"chats": chats_with_companion}
    return render(request, "messenger/chats.html", context)
