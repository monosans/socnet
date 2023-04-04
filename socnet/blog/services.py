from __future__ import annotations

from django.db.models import Count, Prefetch, Q, QuerySet
from django.http import HttpRequest
from django.shortcuts import get_object_or_404

from ..users.models import User
from . import models


def get_posts_preview_qs(request: HttpRequest) -> QuerySet[models.Post]:
    qs = (
        models.Post.objects.only(
            "content",
            "date_created",
            "date_updated",
            "author__image",
            "author__username",
        )
        .annotate(Count("comments", distinct=True), Count("likers", distinct=True))
        .select_related("author")
    )
    if request.user.is_anonymous:
        return qs
    return qs.annotate(is_liked=Q(pk__in=request.user.liked_posts.all()))


def get_subscriptions(username: str, field: str) -> User:
    prefetch = Prefetch(field, User.objects.only("display_name", "image", "username"))
    qs = (
        User.objects.only("username")
        .prefetch_related(prefetch)
        .filter(username=username)
    )
    return get_object_or_404(qs)
