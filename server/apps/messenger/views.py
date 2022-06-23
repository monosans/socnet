from django.contrib.auth.decorators import login_required
from django.db.models import QuerySet
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_http_methods

from ..users.types import AuthedRequest
from . import forms, models


@login_required
@require_http_methods(["GET"])
def chat_list_view(request: AuthedRequest) -> HttpResponse:
    chats: QuerySet[models.Chat] = request.user.chats.prefetch_related(
        "participants", "messages"
    )
    sorted_chats = sorted(
        chats,
        key=lambda x: x.last_message.date.timestamp()
        if x.last_message
        else float("-inf"),
        reverse=True,
    )
    chats_with_companion = (
        (chat, chat.get_companion(request.user)) for chat in sorted_chats
    )
    context = {"chats": chats_with_companion}
    return render(request, "messenger/chat_list.html", context)


@login_required
@require_http_methods(["GET"])
def chat_detail_view(request: AuthedRequest, pk: int) -> HttpResponse:
    chat: models.Chat = get_object_or_404(
        request.user.chats.prefetch_related("messages", "messages__user"),
        pk=pk,
    )
    messages: QuerySet[models.Message] = chat.messages.all()
    form = forms.MessageCreationForm()
    context = {"chat_pk": pk, "messages_": messages, "form": form}
    return render(request, "messenger/chat_detail.html", context)


@login_required
@require_http_methods(["POST"])
def chat_get_or_create_view(request: AuthedRequest, pk: int) -> HttpResponse:
    chat: models.Chat
    chat, created = models.Chat.objects.filter(
        participants__in=[request.user.pk]
    ).get_or_create(participants__in=[pk])
    if created:
        chat.participants.add(request.user.pk, pk)
    return redirect("chat", pk=chat.pk)
