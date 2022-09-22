from __future__ import annotations

from typing import Iterator, Optional, Tuple, TypeVar, Union

from django.contrib.auth import get_user_model
from django.core.paginator import Page, Paginator
from django.db.models import Count, Model, Prefetch, QuerySet
from django.http import HttpRequest
from django.shortcuts import get_object_or_404

from ..users.models import User as UserType
from . import models

User = get_user_model()

TModel = TypeVar("TModel", bound=Model)


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


def get_subscriptions(username: str, field: str) -> UserType:
    prefetch = Prefetch(
        field,
        User.objects.only("username", "first_name", "last_name", "image"),
    )
    qs = User.objects.prefetch_related(prefetch).only("username")
    return get_object_or_404(qs, username=username)


def paginate(
    request: HttpRequest, object_list: QuerySet[TModel], *, per_page: int
) -> Tuple[Page[TModel], Optional[Iterator[Union[str, int]]]]:
    paginator = Paginator(object_list, per_page=per_page)
    try:
        page = int(request.GET["page"])
    except (KeyError, ValueError):
        page = 1
    else:
        if page < 1:
            page = 1
        elif page > paginator.num_pages:
            # If the user sets a page number greater than the
            # last page number, show him the last page.
            page = paginator.num_pages
    posts = paginator.page(page)
    page_range = (
        posts.paginator.get_elided_page_range(page, on_each_side=1, on_ends=1)
        if paginator.num_pages > 1
        else None
    )
    return posts, page_range
