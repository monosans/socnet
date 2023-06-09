from __future__ import annotations

from typing import Optional, TypeVar, Union

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import redirect_to_login
from django.contrib.postgres.search import TrigramWordSimilarity
from django.core.exceptions import PermissionDenied
from django.core.paginator import Page
from django.db.models import Case, Count, Prefetch, Q, QuerySet, When
from django.db.models.functions import Extract
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect, render
from django.utils.translation import gettext as _
from django.views.decorators.http import require_POST
from django.views.generic import CreateView, UpdateView

from ..core.utils import paginate
from ..users.models import User
from ..users.types import AuthedRequest
from . import forms, models, services

TBaseModelForm = TypeVar(
    "TBaseModelForm", bound=Union[forms.PostForm, forms.CommentForm]
)
TPost = TypeVar("TPost", bound=Union[models.Post, models.Comment])


class _BasePostUpdateView(LoginRequiredMixin, UpdateView[TPost, TBaseModelForm]):
    def get_object(self, queryset: Optional[QuerySet[TPost]] = None) -> TPost:
        obj = super().get_object(queryset)
        if obj.author_id != self.request.user.pk:
            raise PermissionDenied
        return obj

    def form_valid(self, form: TBaseModelForm) -> HttpResponse:
        self.object = form.save(commit=False)  # type: ignore[assignment]
        update_fields = (
            (*form.Meta.fields, "date_updated")
            if form.content_has_changed
            else form.Meta.fields
        )
        self.object.save(update_fields=update_fields)
        form.save_m2m()
        return HttpResponseRedirect(self.get_success_url())


class PostUpdateView(_BasePostUpdateView[models.Post, forms.PostForm]):
    model = models.Post
    form_class = forms.PostForm
    template_name = "blog/post_update.html"

    def get_queryset(self) -> QuerySet[models.Post]:
        return super().get_queryset().only("author_id", *self.form_class.Meta.fields)


class CommentUpdateView(_BasePostUpdateView[models.Comment, forms.CommentForm]):
    model = models.Comment
    form_class = forms.CommentForm
    template_name = "blog/comment_update.html"

    def get_queryset(self) -> QuerySet[models.Comment]:
        return (
            super()
            .get_queryset()
            .only("author_id", "post_id", *self.form_class.Meta.fields)
        )


class PostCreateView(LoginRequiredMixin, CreateView[models.Post, forms.PostForm]):
    form_class = forms.PostForm
    template_name = "blog/post_create.html"

    def form_valid(self, form: forms.PostForm) -> HttpResponse:
        form.instance.author = self.request.user  # type: ignore[assignment]
        return super().form_valid(form)


@require_POST
@login_required
def comment_delete_view(request: AuthedRequest, pk: int) -> HttpResponse:
    models.Comment.objects.filter(
        Q(author=request.user) | Q(post__author=request.user), pk=pk
    ).delete()
    redirect_to = request.GET.get("next", request.user)
    return redirect(redirect_to)


@require_POST
@login_required
def post_delete_view(request: AuthedRequest, pk: int) -> HttpResponse:
    models.Post.objects.filter(pk=pk, author=request.user).delete()
    return redirect("blog:user_posts", request.user.username)


def post_view(request: HttpRequest, pk: int) -> HttpResponse:
    if request.method == "POST":
        if request.user.is_anonymous:
            return redirect_to_login(next=request.path)
        form = forms.CommentForm(request.POST)
        if (
            form.is_valid()
            and models.Post.objects.filter(
                Q(allow_commenting=True) | Q(author=request.user), pk=pk
            ).exists()
        ):
            form.instance.author = request.user
            form.instance.post_id = pk
            comment = form.save()
            return redirect(comment)
        messages.error(
            request,
            _("An error occurred while creating the comment. Please try again."),
        )
    else:
        form = forms.CommentForm()
    comments_qs = (
        models.Comment.objects.only(
            "content",
            "post_id",
            "author__display_name",
            "author__image",
            "author__username",
        )
        .annotate_epoch_dates()
        .annotate(Count("likers"))
        .select_related("author")
        .order_by("pk")
    )
    prefetch = Prefetch(
        "comments",
        (
            comments_qs.annotate(is_liked=Q(pk__in=request.user.liked_comments.all()))
            if request.user.is_authenticated
            else comments_qs
        ),
    )
    qs = (
        services.get_posts_preview_qs(request, ("allow_commenting",))
        .prefetch_related(prefetch)
        .filter(pk=pk)
    )
    post = get_object_or_404(qs)
    context = {"post": post, "form": form}
    return render(request, "blog/post.html", context)


def posts_view(request: HttpRequest) -> HttpResponse:
    posts: Optional[Union[QuerySet[models.Post], Page[models.Post]]] = None
    page_range = None
    qs = services.get_posts_preview_qs(request)
    is_search = bool(request.GET.get("q"))
    if is_search:
        form = forms.PostSearchForm(request.GET)
        if form.is_valid():
            q: str = form.cleaned_data["q"]
            posts = (
                qs.annotate(similarity=TrigramWordSimilarity(q, "content"))
                .filter(similarity__gte=0.6)
                .order_by("-pk")
            )
    else:
        form = forms.PostSearchForm()
        if request.user.is_authenticated:
            subscribed_posts = qs.filter(
                author__in=request.user.subscriptions.all()
            ).order_by("-pk")
            posts, page_range = paginate(request, subscribed_posts, per_page=10)
    context = {
        "posts": posts,
        "page_range": page_range,
        "is_search": is_search,
        "form": form,
    }
    return render(request, "blog/posts.html", context)


def liked_posts_view(request: HttpRequest, username: str) -> HttpResponse:
    qs = User.objects.only("display_name", "username").filter(username=username)
    user = get_object_or_404(qs)
    posts = services.get_posts_preview_qs(request).filter(likers=user).order_by("-pk")
    context = {"user": user, "posts": posts}
    return render(request, "blog/liked_posts.html", context)


def user_posts_view(request: HttpRequest, username: str) -> HttpResponse:
    posts = (
        models.Post.objects.only("allow_commenting", "author_id", "content")
        .annotate_epoch_dates()
        .annotate(Count("comments", distinct=True), Count("likers", distinct=True))
        .order_by("-pk")
    )
    prefetch = Prefetch(
        "posts",
        (
            posts.annotate(is_liked=Q(pk__in=request.user.liked_posts.all()))
            if request.user.is_authenticated
            else posts
        ),
    )
    qs = (
        User.objects.only("display_name", "image", "username")
        .prefetch_related(prefetch)
        .filter(username=username)
    )
    user = get_object_or_404(qs)
    context = {"user": user, "posts": user.posts.all()}
    return render(request, "blog/user_posts.html", context)


def subscribers_view(request: HttpRequest, username: str) -> HttpResponse:
    user = services.get_subscriptions(username, "subscribers")
    context = {"user": user, "subscribers": user.subscribers.all()}
    return render(request, "blog/subscribers.html", context)


def subscriptions_view(request: HttpRequest, username: str) -> HttpResponse:
    user = services.get_subscriptions(username, "subscriptions")
    context = {"user": user, "subscriptions": user.subscriptions.all()}
    return render(request, "blog/subscriptions.html", context)


def user_view(request: HttpRequest, username: str) -> HttpResponse:
    qs = (
        User.objects.only(
            "about", "birth_date", "display_name", "image", "location", "username"
        )
        .annotate(
            Count("liked_posts", distinct=True),
            Count("posts", distinct=True),
            Count("subscribers", distinct=True),
            Count("subscriptions", distinct=True),
            date_joined_epoch=Extract("date_joined", "epoch"),
            last_login_epoch=Case(
                When(show_last_login=True, then=Extract("last_login", "epoch")),
                default=None,
            ),
        )
        .filter(username=username)
    )
    user = get_object_or_404(
        qs.annotate(is_subscription=Q(pk__in=request.user.subscriptions.all()))
        if request.user.is_authenticated and request.user.username != username
        else qs
    )
    context = {"user": user}
    return render(request, "blog/user.html", context)
