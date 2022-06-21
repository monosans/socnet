from typing import Union

from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.postgres.search import SearchVector
from django.core.paginator import Page, Paginator
from django.db.models import QuerySet
from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.views.decorators.http import require_http_methods

from ..users.models import User as UserType
from ..users.types import AuthedRequest
from . import forms, models

User = get_user_model()


def get_user(
    request: HttpRequest, username: str, *prefetch_related: str
) -> UserType:
    if (
        len(prefetch_related) < 2
        and request.user.is_authenticated
        and request.user.get_username() == username
    ):
        return request.user
    qs = (
        User.objects.prefetch_related(*prefetch_related)
        if prefetch_related
        else User
    )
    return get_object_or_404(qs, username=username)  # type: ignore[arg-type]


@require_http_methods(["GET", "POST"])
def search_users_view(request: HttpRequest) -> HttpResponse:
    users = None
    if request.method == "POST":
        form = forms.UsersSearchForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            query = data["search_query"].strip()
            fields = data["fields_to_search"]
            users = User.objects.annotate(search=SearchVector(*fields)).filter(
                search=query
            )
    else:
        form = forms.UsersSearchForm()
    context = {"form": form, "users": users}
    return render(request, "main/search_users.html", context)


@login_required
@require_http_methods(["GET"])
def index(request: AuthedRequest) -> HttpResponse:
    return redirect(request.user)


@login_required
@require_http_methods(["GET"])
def subscriber_list_view(
    request: AuthedRequest, username: str
) -> HttpResponse:
    user = get_user(request, username, "subscribers")
    context = {"user": user}
    return render(request, "main/subscriber_list.html", context)


@login_required
@require_http_methods(["GET"])
def subscription_list_view(
    request: AuthedRequest, username: str
) -> HttpResponse:
    user = get_user(request, username, "subscriptions")
    context = {"user": user}
    return render(request, "main/subscription_list.html", context)


@require_http_methods(["GET", "POST"])
def post_detail_view(request: HttpRequest, pk: int) -> HttpResponse:
    if request.method == "POST":
        if not request.user.is_authenticated:
            return redirect("login")
        form = forms.PostCommentCreationForm(request.POST, request.FILES)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post_id = pk
            comment.user = request.user
            comment.save()
            form = forms.PostCommentCreationForm()
    else:
        form = forms.PostCommentCreationForm()
    post = get_object_or_404(
        models.Post.objects.select_related("user").prefetch_related(
            "likers", "comments", "comments__user", "comments__likers"
        ),
        pk=pk,
    )
    context = {"post": post, "form": form}
    return render(request, "main/post_detail.html", context)


@login_required
@require_http_methods(["POST"])
def post_delete_view(request: AuthedRequest, pk: int) -> HttpResponse:
    post = get_object_or_404(models.Post, pk=pk)
    if post.user != request.user:
        return redirect(post)
    post.delete()
    return redirect(request.user)


@require_http_methods(["GET", "POST"])
def post_list_view(request: HttpRequest) -> HttpResponse:
    posts: Union[QuerySet[models.Post], Page[models.Post], None] = None
    page_range = None
    if request.method == "POST":
        form = forms.PostsSearchForm(request.POST)
        if form.is_valid():
            query = form.cleaned_data["search_query"]
            posts = (
                models.Post.objects.select_related("user")
                .prefetch_related("likers", "comments")
                .filter(text__search=query)
            )
    else:
        form = forms.PostsSearchForm()
        if request.user.is_authenticated:
            p = (
                models.Post.objects.select_related("user")
                .prefetch_related("likers", "comments")
                .filter(user__in=request.user.subscriptions.all())
            )
            page = request.GET.get("page", "1")
            paginator = Paginator(p, 5)
            if paginator.num_pages < int(page):
                # If the user sets a page number greater than the
                # last page number, we redirect him to the last page.
                url = "{}?page={}".format(
                    reverse("posts"), paginator.num_pages
                )
                return redirect(url)
            posts = paginator.get_page(page)
            if paginator.num_pages > 1:
                page_range = posts.paginator.get_elided_page_range(
                    page, on_each_side=1, on_ends=1
                )
    context = {"posts": posts, "page_range": page_range, "form": form}
    return render(request, "main/post_list.html", context)


@require_http_methods(["GET", "POST"])
def user_detail_view(request: HttpRequest, username: str) -> HttpResponse:
    user = get_user(
        request,
        username,
        "liked_posts",
        "posts",
        "posts__comments",
        "posts__likers",
        "subscribers",
        "subscriptions",
    )
    post_creation_form = None
    user_change_form = None
    if request.user.is_authenticated and request.user == user:
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
            elif form_type == "user_change_form":
                user_change_form = forms.UserChangeForm(
                    request.POST, request.FILES, instance=request.user
                )
                if user_change_form.is_valid():
                    user_change_form.save()
        else:
            post_creation_form = forms.PostCreationForm()
            user_change_form = forms.UserChangeForm(instance=request.user)
    context = {
        "user": user,
        "post_creation_form": post_creation_form,
        "user_change_form": user_change_form,
    }
    return render(request, "main/user_detail.html", context)


@login_required
@require_http_methods(["POST"])
def post_comment_delete_view(request: AuthedRequest, pk: int) -> HttpResponse:
    comment = get_object_or_404(models.PostComment, pk=pk)
    if comment.user == request.user:
        comment.delete()
    return redirect(comment.post)


@require_http_methods(["GET"])
def liked_post_list_view(request: HttpRequest, username: str) -> HttpResponse:
    user = get_user(
        request,
        username,
        "liked_posts",
        "liked_posts__comments",
        "liked_posts__likers",
        "liked_posts__user",
    )
    context = {"user": user, "posts": user.liked_posts.all()}
    return render(request, "main/liked_post_list.html", context)
