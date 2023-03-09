from __future__ import annotations

from django.contrib.auth.decorators import login_required
from django.db.models import OuterRef, Q, Subquery
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render
from django.views.decorators.http import require_safe

from ..users.models import User
from ..users.types import AuthedRequest
from . import forms, models


@require_safe
@login_required
def chat_view(request: AuthedRequest, username: str) -> HttpResponse:
    qs = User.objects.only("username", "display_name", "image").filter(
        username=username
    )
    interlocutor = get_object_or_404(qs)
    messages = (
        models.Message.objects.only(
            "content",
            "date_created",
            "sender__display_name",
            "sender__image",
            "sender__username",
        )
        .select_related("sender")
        .filter(
            Q(sender=request.user, recipient=interlocutor)
            | Q(sender=interlocutor, recipient=request.user)
        )
    )
    form = forms.MessageCreationForm()
    context = {"messages_": messages, "interlocutor": interlocutor, "form": form}
    return render(request, "messenger/chat.html", context)


@require_safe
@login_required
def chats_view(request: AuthedRequest) -> HttpResponse:
    last_message = models.Message.objects.filter(
        Q(sender=request.user, recipient_id=OuterRef("pk"))
        | Q(sender_id=OuterRef("pk"), recipient=request.user)
    ).order_by("-pk")
    chats = (
        User.objects.distinct()
        .only("username", "display_name", "image")
        .annotate(
            last_message_date=Subquery(last_message.values("date_created")[:1]),
            last_message_content=Subquery(last_message.values("content")[:1]),
        )
        .filter(
            Q(incoming_messages__sender=request.user)
            | Q(outgoing_messages__recipient=request.user)
        )
        .order_by("-last_message_date")
    )
    context = {"chats": chats}
    return render(request, "messenger/chats.html", context)
