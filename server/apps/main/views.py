from typing import List, Optional, Union

from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import redirect_to_login
from django.contrib.postgres.search import SearchVector
from django.core.paginator import Page, Paginator
from django.db.models import Count, Prefetch, QuerySet
from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.utils.translation import gettext as _
from django.views.decorators.http import require_http_methods

from ..users.models import User as UserType
from ..users.types import AuthedRequest
from . import forms, models

User = get_user_model()


@login_required
@require_http_methods(["GET"])
def index(request: AuthedRequest) -> HttpResponse:
    return redirect(request.user)


@require_http_methods(["GET", "POST"])
def user_view(request: HttpRequest, username: str) -> HttpResponse:
    post_creation_form = None
    user_change_form = None
    if (
        request.user.is_authenticated
        and request.user.get_username() == username
    ):
        if request.method == "POST":
            form_type = request.POST["_form_type"]
            if form_type == "post_creation_form":
                post_creation_form = forms.PostCreationForm(
                    request.POST, request.FILES
                )
                if post_creation_form.is_valid():
                    post = post_creation_form.save(commit=False)
                    post.user = request.user
                    post.save()
                    post_creation_form = forms.PostCreationForm()
                else:
                    message = "{} {}".format(
                        _("An error occurred while creating the post."),
                        _("Please try again."),
                    )
                    messages.error(request, message)
            elif form_type == "user_change_form":
                user_change_form = forms.UserChangeForm(
                    request.POST, request.FILES, instance=request.user
                )
                if user_change_form.is_valid():
                    user_change_form.save()
                else:
                    message = "{} {}".format(
                        _("An error occurred while saving the profile."),
                        _("Please try again."),
                    )
                    messages.error(request, message)
        if post_creation_form is None:
            post_creation_form = forms.PostCreationForm()
        if user_change_form is None:
            user_change_form = forms.UserChangeForm(instance=request.user)
    users = User.objects.only("pk")
    subscribers_prefetch = Prefetch("subscribers", users)
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
    posts_prefetch = Prefetch("posts", posts_prefetch_qs)
    user: UserType = get_object_or_404(
        User.objects.annotate(
            Count("subscriptions", distinct=True),
            Count("liked_posts", distinct=True),
        )
        .prefetch_related(subscribers_prefetch, posts_prefetch)
        .only(
            "username",
            "image",
            "first_name",
            "last_name",
            "birth_date",
            "location",
            "about",
        ),
        username=username,
    )
    context = {
        "user": user,
        "post_creation_form": post_creation_form,
        "user_change_form": user_change_form,
    }
    return render(request, "main/user.html", context)


@require_http_methods(["GET", "POST"])
def users_search_view(request: HttpRequest) -> HttpResponse:
    users: Optional[QuerySet[UserType]] = None
    if request.method == "POST":
        form = forms.UsersSearchForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            query: str = data["search_query"]
            fields: List[str] = data["fields_to_search"]
            users = (
                User.objects.annotate(search=SearchVector(*fields))
                .filter(search=query.strip())
                .only("username", "first_name", "last_name", "image")
            )
    else:
        form = forms.UsersSearchForm()
    context = {"form": form, "users": users}
    return render(request, "main/users_search.html", context)


@login_required
@require_http_methods(["GET"])
def subscriptions_view(request: AuthedRequest, username: str) -> HttpResponse:
    prefetch = Prefetch(
        "subscriptions",
        User.objects.only("username", "first_name", "last_name", "image"),
    )
    user = get_object_or_404(
        User.objects.prefetch_related(prefetch).only("username"),
        username=username,
    )
    context = {"user": user}
    return render(request, "main/subscriptions.html", context)


@login_required
@require_http_methods(["GET"])
def subscribers_view(request: AuthedRequest, username: str) -> HttpResponse:
    prefetch = Prefetch(
        "subscribers",
        User.objects.only("username", "first_name", "last_name", "image"),
    )
    user = get_object_or_404(
        User.objects.prefetch_related(prefetch).only("username"),
        username=username,
    )
    context = {"user": user}
    return render(request, "main/subscribers.html", context)


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
    return render(request, "main/post.html", context)


@require_http_methods(["GET", "POST"])
def posts_view(request: HttpRequest) -> HttpResponse:
    posts: Union[QuerySet[models.Post], Page[models.Post], None] = None
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
    if request.method == "POST":
        form = forms.PostsSearchForm(request.POST)
        if form.is_valid():
            query: str = form.cleaned_data["search_query"]
            posts = qs.filter(text__search=query)
    else:
        form = forms.PostsSearchForm()
        if request.user.is_authenticated:
            p: QuerySet[models.Post] = qs.filter(
                user__in=request.user.subscriptions.all()
            )
            paginator = Paginator(p, per_page=5)
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
    return render(request, "main/posts.html", context)


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
    user: UserType = get_object_or_404(
        User.objects.prefetch_related(prefetch).only("username"),
        username=username,
    )
    context = {"user": user, "posts": user.liked_posts.all()}
    return render(request, "main/liked_posts.html", context)


@login_required
@require_http_methods(["POST"])
def post_delete_view(request: AuthedRequest, pk: int) -> HttpResponse:
    post: models.Post = get_object_or_404(request.user.posts.only("pk"), pk=pk)
    post.delete()
    return redirect(request.user)


@login_required
@require_http_methods(["POST"])
def post_comment_delete_view(request: AuthedRequest, pk: int) -> HttpResponse:
    comment: models.PostComment = get_object_or_404(
        request.user.post_comments.only("pk"), pk=pk
    )
    comment.delete()
    return redirect(comment.post)
