from __future__ import annotations

from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.db.models import Prefetch, QuerySet
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_http_methods

from ..users.models import User as UserType
from ..users.types import AuthedRequest
from . import forms, models

User: type[UserType] = get_user_model()


@login_required
@require_http_methods(["GET"])
def chat_view(request: AuthedRequest, pk: int) -> HttpResponse:
    prefetch = Prefetch(
        "messages",
        models.Message.objects.select_related("user").only(
            "text", "date", "chat_id", "user__username", "user__image"
        ),
    )
    chat: models.Chat = get_object_or_404(
        request.user.chats.prefetch_related(prefetch).only("pk"), pk=pk
    )
    form = forms.MessageCreationForm()
    context = {"chat": chat, "form": form}
    return render(request, "messenger/chat.html", context)


@login_required
@require_http_methods(["GET"])
def chats_view(request: AuthedRequest) -> HttpResponse:
    prefetches = (
        Prefetch(
            "participants",
            User.objects.only("username", "image", "first_name", "last_name"),
        ),
        Prefetch(
            "messages",
            models.Message.objects.order_by("chat_id", "-date")
            .distinct("chat_id")
            .only("text", "date", "chat_id"),
        ),
    )
    chats: QuerySet[models.Chat] = request.user.chats.prefetch_related(
        *prefetches
    )
    chats_with_companion = (
        (chat, chat.get_companion(request.user)) for chat in chats
    )
    context = {"chats": chats_with_companion}
    return render(request, "messenger/chats.html", context)


@login_required
@require_http_methods(["POST"])
def chat_get_or_create_view(request: AuthedRequest, pk: int) -> HttpResponse:
    chat: models.Chat
    chat, created = models.Chat.objects.filter(
        participants__in=[request.user.pk]
    ).get_or_create(participants__in=[pk])
    if created:
        chat.participants.set([request.user.pk, pk])
    return redirect(chat)
