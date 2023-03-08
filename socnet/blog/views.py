from __future__ import annotations

from typing import Optional, TypeVar, Union

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import redirect_to_login
from django.contrib.postgres.search import SearchRank
from django.core.exceptions import PermissionDenied
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
from django.views.generic import UpdateView

from ..core.utils import paginate
from ..users.models import User
from ..users.types import AuthedRequest
from . import forms, models, services

T_BaseModelForm = TypeVar(
    "T_BaseModelForm", bound=Union[forms.PostForm, forms.PostCommentForm]
)
T_Post = TypeVar("T_Post", bound=Union[models.Post, models.PostComment])


class _BaseEditPostView(LoginRequiredMixin, UpdateView[T_Post, T_BaseModelForm]):
    def get_object(self, queryset: Optional[QuerySet[T_Post]] = None) -> T_Post:
        obj = super().get_object(queryset)
        if obj.author_id != self.request.user.pk:
            raise PermissionDenied
        return obj

    def form_valid(self, form: T_BaseModelForm) -> HttpResponse:
        self.object = form.save(commit=False)  # type: ignore[assignment]
        self.object.save(update_fields=(*form.Meta.fields, "date_updated"))
        form.save_m2m()
        return redirect(self.object)


class EditPostView(_BaseEditPostView[models.Post, forms.PostForm]):
    model = models.Post
    form_class = forms.PostForm
    template_name = "blog/edit_post.html"

    def get_queryset(self) -> QuerySet[models.Post]:
        return super().get_queryset().only("author_id", *self.form_class.Meta.fields)


class EditPostCommentView(_BaseEditPostView[models.PostComment, forms.PostCommentForm]):
    model = models.PostComment
    form_class = forms.PostCommentForm
    template_name = "blog/edit_comment.html"

    def get_queryset(self) -> QuerySet[models.PostComment]:
        return (
            super()
            .get_queryset()
            .only("author_id", "post_id", *self.form_class.Meta.fields)
        )


@require_http_methods(["GET", "HEAD", "POST"])
@login_required
def create_post_view(request: AuthedRequest) -> HttpResponse:
    if request.method == "POST":
        form = forms.PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect(post)
    else:
        form = forms.PostForm()
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
        form = forms.PostCommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post_id = pk
            comment.author = request.user
            comment.save()
            form = forms.PostCommentForm()
        else:
            message = "{} {}".format(
                _("An error occurred while creating the comment."),
                _("Please try again."),
            )
            messages.error(request, message)
    else:
        form = forms.PostCommentForm()
    comments_qs = (
        models.PostComment.objects.annotate(Count("likers"))
        .select_related("author")
        .order_by("pk")
        .only("date_created", "post_id", "content", "author__image", "author__username")
    )
    if request.user.is_authenticated:
        comments_qs = comments_qs.annotate(  # type: ignore[assignment]
            is_liked=Q(pk__in=request.user.liked_comments.all())
        )
    prefetch = Prefetch("comments", comments_qs)
    qs = services.get_posts_preview_qs(request).filter(pk=pk).prefetch_related(prefetch)
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
            rank = SearchRank(vector="content", query=query)
            posts = qs.annotate(rank=rank).filter(rank__gt=0).order_by("-rank", "-pk")
    else:
        form = forms.PostSearchForm()
        if request.user.is_authenticated:
            subscribed_posts = qs.filter(
                author__in=request.user.subscriptions.all()
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
        .only("date_created", "content", "author_id")
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
        .only("about", "birth_date", "display_name", "image", "location", "username")
    )
    if request.user.is_authenticated:
        qs = qs.annotate(  # type: ignore[assignment]
            is_subscription=Q(pk__in=request.user.subscriptions.all())
        )
    user = get_object_or_404(qs)
    context = {"user": user}
    return render(request, "blog/user.html", context)
