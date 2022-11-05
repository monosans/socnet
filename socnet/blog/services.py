from __future__ import annotations

from django.db.models import Count, Prefetch, QuerySet
from django.http import HttpRequest
from django.shortcuts import get_object_or_404

from ..users.models import User
from . import models


def get_posts_preview_qs(request: HttpRequest) -> QuerySet[models.Post]:
    qs = models.Post.objects.select_related("user").only(
        "date", "text", "image", "user__username", "user__image"
    )
    if request.user.is_anonymous:
        return qs.annotate(
            Count("comments", distinct=True), Count("likers", distinct=True)
        )
    return qs.annotate(Count("comments")).prefetch_related(
        Prefetch("likers", User.objects.only("pk"))
    )


def get_subscriptions(username: str, field: str) -> User:
    prefetch = Prefetch(
        field, User.objects.only("username", "display_name", "image")
    )
    qs = User.objects.prefetch_related(prefetch).only("username")
    return get_object_or_404(qs, username=username)
