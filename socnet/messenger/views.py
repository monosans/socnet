from __future__ import annotations

from django.contrib.auth.decorators import login_required
from django.db.models import OuterRef, Q, Subquery
from django.db.models.functions import Extract, Substr
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render

from ..users.models import User
from ..users.types import AuthedRequest
from . import forms, models


@login_required
def chat_view(request: AuthedRequest, username: str) -> HttpResponse:
    qs = User.objects.only("display_name", "username", "image").filter(
        username=username
    )
    interlocutor = get_object_or_404(qs)
    messages = (
        models.Message.objects.only(
            "content", "sender__display_name", "sender__image", "sender__username"
        )
        .annotate(date_created_epoch=Extract("date_created", "epoch"))
        .select_related("sender")
        .filter(
            Q(sender=request.user, recipient=interlocutor)
            | Q(sender=interlocutor, recipient=request.user)
        )
        .order_by("pk")
    )
    form = forms.MessageCreationForm()
    context = {"messages_": messages, "interlocutor": interlocutor, "form": form}
    return render(request, "messenger/chat.html", context)


@login_required
def chats_view(request: AuthedRequest) -> HttpResponse:
    last_message = (
        models.Message.objects.annotate(
            date_created_epoch=Extract("date_created", "epoch"),
            truncated_content=Substr("content", 1, 30),
        )
        .filter(
            Q(sender=request.user, recipient_id=OuterRef("pk"))
            | Q(sender_id=OuterRef("pk"), recipient=request.user)
        )
        .order_by("-pk")
    )
    chats = (
        User.objects.distinct()
        .only("display_name", "image", "username")
        .annotate(
            last_message_date_epoch=Subquery(
                last_message.values("date_created_epoch")[:1]
            ),
            last_message_truncated_content=Subquery(
                last_message.values("truncated_content")[:1]
            ),
        )
        .filter(
            Q(incoming_messages__sender=request.user)
            | Q(outgoing_messages__recipient=request.user)
        )
        .order_by(-Subquery(last_message.values("pk")[:1]))
    )
    context = {"chats": chats}
    return render(request, "messenger/chats.html", context)
