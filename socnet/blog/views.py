from __future__ import annotations

from typing import Optional, Union

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import redirect_to_login
from django.contrib.postgres.search import SearchRank
from django.core.paginator import Page
from django.db.models import Count, Prefetch, Q, QuerySet
from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.utils.translation import gettext as _
from django.views.decorators.http import (
    require_http_methods,
    require_POST,
    require_safe,
)

from ..core.utils import paginate
from ..users.models import User
from ..users.types import AuthedRequest
from . import forms, models, services


@require_http_methods(["GET", "HEAD", "POST"])
@login_required
def create_post_view(request: AuthedRequest) -> HttpResponse:
    if request.method == "POST":
        form = forms.PostCreationForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.user = request.user
            post.save()
            return redirect(post)
    else:
        form = forms.PostCreationForm()
    context = {"form": form}
    return render(request, "blog/create_post.html", context)


@require_POST
@login_required
def post_comment_delete_view(request: AuthedRequest, pk: int) -> HttpResponse:
    request.user.post_comments.filter(pk=pk).delete()
    redirect_to = request.GET.get("next", request.user)
    return redirect(redirect_to)


@require_POST
@login_required
def post_delete_view(request: AuthedRequest, pk: int) -> HttpResponse:
    request.user.posts.filter(pk=pk).delete()
    url = reverse("blog:user_posts", args=(request.user.get_username(),))
    return redirect(url)


@require_http_methods(["GET", "HEAD", "POST"])
def post_view(request: HttpRequest, pk: int) -> HttpResponse:
    if request.method == "POST":
        if request.user.is_anonymous:
            return redirect_to_login(next=request.path)
        form = forms.PostCommentCreationForm(request.POST, request.FILES)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post_id = pk
            comment.user = request.user
            comment.save()
            form = forms.PostCommentCreationForm()
        else:
            # pylint: disable-next=consider-using-f-string
            message = "{} {}".format(
                _("An error occurred while creating the comment."),
                _("Please try again."),
            )
            messages.error(request, message)
    else:
        form = forms.PostCommentCreationForm()
    comments_qs = (
        models.PostComment.objects.annotate(Count("likers"))
        .select_related("user")
        .order_by("pk")
        .only(
            "date", "image", "post_id", "text", "user__image", "user__username"
        )
    )
    if request.user.is_authenticated:
        comments_qs = comments_qs.annotate(  # type: ignore[assignment]
            is_liked=Q(pk__in=request.user.liked_comments.all())
        )
    prefetch = Prefetch("comments", comments_qs)
    qs = (
        services.get_posts_preview_qs(request)
        .filter(pk=pk)
        .prefetch_related(prefetch)
    )
    post = get_object_or_404(qs)
    context = {"post": post, "form": form}
    return render(request, "blog/post.html", context)


@require_safe
def posts_view(request: HttpRequest) -> HttpResponse:
    posts: Optional[Union[QuerySet[models.Post], Page[models.Post]]] = None
    page_range = None
    qs = services.get_posts_preview_qs(request)
    if "q" in request.GET:
        form = forms.PostSearchForm(request.GET)
        if form.is_valid():
            query: str = form.cleaned_data["q"]
            rank = SearchRank(vector="text", query=query)
            posts = (
                qs.annotate(rank=rank)
                .filter(rank__gt=0)
                .order_by("-rank", "-pk")
            )
    else:
        form = forms.PostSearchForm()
        if request.user.is_authenticated:
            subscribed_posts = qs.filter(
                user__in=request.user.subscriptions.all()
            ).order_by("-pk")
            posts, page_range = paginate(request, subscribed_posts, per_page=5)
    context = {"posts": posts, "page_range": page_range, "form": form}
    return render(request, "blog/posts.html", context)


@require_safe
def liked_posts_view(request: HttpRequest, username: str) -> HttpResponse:
    prefetch_qs = services.get_posts_preview_qs(request).order_by("-pk")
    prefetch = Prefetch("liked_posts", prefetch_qs)
    qs = (
        User.objects.filter(username=username)
        .prefetch_related(prefetch)
        .only("username")
    )
    user = get_object_or_404(qs)
    context = {"user": user}
    return render(request, "blog/liked_posts.html", context)


@require_safe
def user_posts_view(request: HttpRequest, username: str) -> HttpResponse:
    posts = (
        models.Post.objects.annotate(
            Count("comments", distinct=True), Count("likers", distinct=True)
        )
        .order_by("-pk")
        .only("date", "image", "text", "user_id")
    )
    if request.user.is_authenticated:
        posts = posts.annotate(  # type: ignore[assignment]
            is_liked=Q(pk__in=request.user.liked_posts.all())
        )
    prefetch = Prefetch("posts", posts)
    qs = (
        User.objects.filter(username=username)
        .prefetch_related(prefetch)
        .only("image", "username")
    )
    user = get_object_or_404(qs)
    context = {"user": user}
    return render(request, "blog/user_posts.html", context)


@require_safe
def subscribers_view(request: HttpRequest, username: str) -> HttpResponse:
    user = services.get_subscriptions(username, "subscribers")
    context = {"user": user}
    return render(request, "blog/subscribers.html", context)


@require_safe
def subscriptions_view(request: HttpRequest, username: str) -> HttpResponse:
    user = services.get_subscriptions(username, "subscriptions")
    context = {"user": user}
    return render(request, "blog/subscriptions.html", context)


@require_safe
def user_view(request: HttpRequest, username: str) -> HttpResponse:
    qs = (
        User.objects.filter(username=username)
        .annotate(
            Count("liked_posts", distinct=True),
            Count("posts", distinct=True),
            Count("subscribers", distinct=True),
            Count("subscriptions", distinct=True),
        )
        .only(
            "about",
            "birth_date",
            "display_name",
            "image",
            "location",
            "username",
        )
    )
    if request.user.is_authenticated:
        qs = qs.annotate(  # type: ignore[assignment]
            is_subscription=Q(pk__in=request.user.subscriptions.all())
        )
    user = get_object_or_404(qs)
    context = {"user": user}
    return render(request, "blog/user.html", context)
