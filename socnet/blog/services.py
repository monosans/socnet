from __future__ import annotations

from typing import TYPE_CHECKING

from django.db.models import Count, Prefetch, Q
from django.shortcuts import get_object_or_404

from socnet.blog import models
from socnet.users.models import User

if TYPE_CHECKING:
    from collections.abc import Iterable

    from django.db.models import QuerySet

    from socnet.core.types import HttpRequest


def get_posts_preview_qs(
    request: HttpRequest, extra_fields: Iterable[str] = ()
) -> QuerySet[models.Post]:
    qs = (
        models.Post.objects
        .only(
            "allow_commenting",
            "content",
            "author__display_name",
            "author__image",
            "author__username",
            *extra_fields,
        )
        .annotate_epoch_dates()
        .annotate(
            Count("comments", distinct=True), Count("likers", distinct=True)
        )
        .select_related("author")
    )
    if request.user.is_anonymous:
        return qs
    return qs.annotate(is_liked=Q(pk__in=request.user.liked_posts.all()))


def get_subscriptions(username: str, field: str) -> User:
    prefetch = Prefetch(
        field,
        User.objects.only("display_name", "image", "username").order_by(
            "username"
        ),
    )
    qs = (
        User.objects
        .only("display_name", "username")
        .prefetch_related(prefetch)
        .filter(username=username)
    )
    return get_object_or_404(qs)
