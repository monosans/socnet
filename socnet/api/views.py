from __future__ import annotations

from typing import Literal

from django.shortcuts import get_object_or_404
from ninja import NinjaAPI
from ninja.security import django_auth
from pydantic import PositiveInt

from socnet.blog.models import Comment, Post
from socnet.core.types import AuthedRequest
from socnet.users.models import User

api = NinjaAPI(title="SocNet", auth=django_auth)


@api.post("/posts/{post_id}/likes", response={201: None})
def add_post_like(
    request: AuthedRequest, post_id: PositiveInt
) -> tuple[Literal[201], None]:
    post = get_object_or_404(Post, pk=post_id)
    post.likers.add(request.user)
    return 201, None


@api.delete("/posts/{post_id}/likes", response={204: None})
def remove_post_like(
    request: AuthedRequest, post_id: PositiveInt
) -> tuple[Literal[204], None]:
    post = get_object_or_404(Post, pk=post_id)
    post.likers.remove(request.user)
    return 204, None


@api.post("/comments/{comment_id}/likes", response={201: None})
def add_comment_like(
    request: AuthedRequest, comment_id: PositiveInt
) -> tuple[Literal[201], None]:
    comment = get_object_or_404(Comment, pk=comment_id)
    comment.likers.add(request.user)
    return 201, None


@api.delete("/comments/{comment_id}/likes", response={204: None})
def remove_comment_like(
    request: AuthedRequest, comment_id: PositiveInt
) -> tuple[Literal[204], None]:
    comment = get_object_or_404(Comment, pk=comment_id)
    comment.likers.remove(request.user)
    return 204, None


@api.post("/users/{username}/subscriptions", response={201: None})
def add_subscription(
    request: AuthedRequest, username: str
) -> tuple[Literal[201], None]:
    to_user = get_object_or_404(User.objects.only("pk"), username=username)
    request.user.subscriptions.add(to_user)
    return 201, None


@api.delete("/users/{username}/subscriptions", response={204: None})
def remove_subscription(
    request: AuthedRequest, username: str
) -> tuple[Literal[204], None]:
    to_user = get_object_or_404(User, username=username)
    request.user.subscriptions.remove(to_user)
    return 204, None
