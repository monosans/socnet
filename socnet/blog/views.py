from __future__ import annotations

from typing import Iterable, Optional

from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import redirect_to_login
from django.contrib.postgres.search import SearchRank
from django.core.paginator import Paginator
from django.db.models import Count, Prefetch
from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.utils.translation import gettext as _
from django.views.decorators.http import require_http_methods

from ..users.types import AuthedRequest
from . import forms, models

User = get_user_model()


@require_http_methods(["GET"])
def user_view(request: HttpRequest, username: str) -> HttpResponse:
    users = User.objects.only("pk")
    posts_prefetch_qs = models.Post.objects.only(
        "user_id", "date", "text", "image"
    )
    posts_prefetch_qs = (
        posts_prefetch_qs.annotate(
            Count("comments", distinct=True), Count("likers", distinct=True)
        )
        if request.user.is_anonymous
        else posts_prefetch_qs.annotate(Count("comments")).prefetch_related(
            Prefetch("likers", users)
        )
    )
    qs = (
        User.objects.annotate(
            Count("subscriptions", distinct=True),
            Count("liked_posts", distinct=True),
        )
        .prefetch_related(
            Prefetch("subscribers", users),
            Prefetch("posts", posts_prefetch_qs),
        )
        .only(
            "username",
            "image",
            "first_name",
            "last_name",
            "birth_date",
            "location",
            "about",
        )
    )
    user = get_object_or_404(qs, username=username)
    context = {"user": user}
    return render(request, "blog/user.html", context)


@login_required
@require_http_methods(["GET", "POST"])
def post_create_view(request: AuthedRequest) -> HttpResponse:
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
    return render(request, "blog/post_create.html", context)


@login_required
@require_http_methods(["GET"])
def subscriptions_view(request: AuthedRequest, username: str) -> HttpResponse:
    prefetch = Prefetch(
        "subscriptions",
        User.objects.only("username", "first_name", "last_name", "image"),
    )
    qs = User.objects.prefetch_related(prefetch).only("username")
    user = get_object_or_404(qs, username=username)
    context = {"user": user}
    return render(request, "blog/subscriptions.html", context)


@login_required
@require_http_methods(["GET"])
def subscribers_view(request: AuthedRequest, username: str) -> HttpResponse:
    prefetch = Prefetch(
        "subscribers",
        User.objects.only("username", "first_name", "last_name", "image"),
    )
    qs = User.objects.prefetch_related(prefetch).only("username")
    user = get_object_or_404(qs, username=username)
    context = {"user": user}
    return render(request, "blog/subscribers.html", context)


@require_http_methods(["GET", "POST"])
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
    prefetch_qs = models.PostComment.objects.select_related("user").only(
        "post_id", "text", "image", "date", "user__username", "user__image"
    )
    qs = models.Post.objects.select_related("user").only(
        "text", "image", "date", "user__username", "user__image"
    )
    if request.user.is_anonymous:
        prefetch_qs = prefetch_qs.annotate(Count("likers"))
        qs = qs.annotate(Count("likers"))
    else:
        users = User.objects.only("pk")
        prefetch_qs = prefetch_qs.prefetch_related(Prefetch("likers", users))
        qs = qs.prefetch_related(Prefetch("likers", users))
    prefetch = Prefetch("comments", prefetch_qs)
    qs = qs.prefetch_related(prefetch)
    post = get_object_or_404(qs, pk=pk)
    context = {"post": post, "form": form}
    return render(request, "blog/post.html", context)


@require_http_methods(["GET"])
def posts_view(request: HttpRequest) -> HttpResponse:
    posts: Optional[Iterable[models.Post]] = None
    page_range = None
    qs = models.Post.objects.select_related("user").only(
        "date", "text", "image", "user__username", "user__image"
    )
    qs = (
        qs.annotate(
            Count("comments", distinct=True), Count("likers", distinct=True)
        )
        if request.user.is_anonymous
        else qs.annotate(Count("comments")).prefetch_related(
            Prefetch("likers", User.objects.only("pk"))
        )
    )
    if request.GET:
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
            paginator = Paginator(subscribed_posts, per_page=5)
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
            if paginator.num_pages > 1:
                page_range = posts.paginator.get_elided_page_range(
                    page, on_each_side=1, on_ends=1
                )
    context = {"posts": posts, "page_range": page_range, "form": form}
    return render(request, "blog/posts.html", context)


@require_http_methods(["GET"])
def liked_posts_view(request: HttpRequest, username: str) -> HttpResponse:
    prefetch_qs = models.Post.objects.select_related("user").only(
        "date", "image", "text", "user__username", "user__image"
    )
    prefetch_qs = (
        prefetch_qs.annotate(
            Count("likers", distinct=True), Count("comments", distinct=True)
        )
        if request.user.is_anonymous
        else prefetch_qs.annotate(Count("comments")).prefetch_related(
            Prefetch("likers", User.objects.only("id"))
        )
    )
    prefetch = Prefetch("liked_posts", prefetch_qs)
    qs = User.objects.prefetch_related(prefetch).only("username")
    user = get_object_or_404(qs, username=username)
    context = {"user": user, "posts": user.liked_posts.all()}
    return render(request, "blog/liked_posts.html", context)


@login_required
@require_http_methods(["POST"])
def post_delete_view(request: AuthedRequest, pk: int) -> HttpResponse:
    qs = request.user.posts.only("pk")
    post = get_object_or_404(qs, pk=pk)
    post.delete()
    return redirect(request.user)


@login_required
@require_http_methods(["POST"])
def post_comment_delete_view(request: AuthedRequest, pk: int) -> HttpResponse:
    qs = request.user.post_comments.only("pk")
    comment = get_object_or_404(qs, pk=pk)
    comment.delete()
    return redirect(comment.post)
