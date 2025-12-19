from __future__ import annotations

from typing import TYPE_CHECKING

from django.contrib.auth.decorators import login_required
from django.contrib.postgres.search import TrigramWordSimilarity
from django.db.models import OuterRef, Q, Subquery
from django.db.models.functions import Extract, Substr
from django.shortcuts import get_object_or_404, render

from socnet.messenger import forms, models
from socnet.users.models import User

if TYPE_CHECKING:
    from typing import Any

    from django.http import HttpResponse

    from socnet.core.types import AuthedRequest


@login_required
def chat_view(request: AuthedRequest, username: str) -> HttpResponse:
    qs = User.objects.only("display_name", "username", "image").filter(
        username=username
    )
    interlocutor = get_object_or_404(qs)
    messages = (
        models.Message.objects
        .only(
            "content",
            "sender__display_name",
            "sender__image",
            "sender__username",
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
    context = {
        "messages_": messages,
        "interlocutor": interlocutor,
        "form": form,
    }
    return render(request, "messenger/chat.html", context)


@login_required
def chats_view(request: AuthedRequest) -> HttpResponse:
    if request.GET.get("q"):
        form = forms.MessageSearchForm(request.GET)
        if form.is_valid():
            q: str = form.cleaned_data["q"]
            messages = (
                models.Message.objects
                .only(
                    "recipient__display_name",
                    "recipient__image",
                    "recipient__username",
                    "sender__display_name",
                    "sender__image",
                    "sender__username",
                )
                .annotate(
                    date_created_epoch=Extract("date_created", "epoch"),
                    similarity=TrigramWordSimilarity(q, "content"),
                    truncated_content=Substr("content", 1, 30),
                )
                .select_related("recipient", "sender")
                .filter(
                    Q(sender=request.user) | Q(recipient=request.user),
                    similarity__gte=0.6,
                )
                .order_by("-pk")
            )
            msgs_with_interlocutor = [
                (
                    msg,
                    msg.recipient if msg.sender == request.user else msg.sender,
                )
                for msg in messages
            ]
        else:
            msgs_with_interlocutor = None
        context: dict[str, Any] = {
            "messages_": msgs_with_interlocutor,
            "form": form,
        }
        return render(request, "messenger/messages_search.html", context)
    form = forms.MessageSearchForm()
    last_message = (
        models.Message.objects
        .annotate(
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
        User.objects
        .distinct()
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
        .order_by("-last_message_date_epoch")
    )
    context = {"chats": chats, "form": form}
    return render(request, "messenger/chats.html", context)
