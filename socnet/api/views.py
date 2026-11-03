from __future__ import annotations

from django.shortcuts import get_object_or_404
from django.utils.translation import gettext as _
from ninja import NinjaAPI, Status
from ninja.errors import HttpError
from ninja.security import django_auth
from pydantic import PositiveInt

from socnet.blog.models import Comment, Post
from socnet.core.types import AuthedRequest
from socnet.users.models import User

api = NinjaAPI(title="Socnet", auth=django_auth)


@api.post("/posts/{post_id}/likes", response={201: None})
def add_post_like(request: AuthedRequest, post_id: PositiveInt) -> Status[None]:
    post = get_object_or_404(Post, pk=post_id)
    post.likers.add(request.user)
    return Status(201, None)


@api.delete("/posts/{post_id}/likes", response={204: None})
def remove_post_like(request: AuthedRequest, post_id: PositiveInt) -> Status[None]:
    post = get_object_or_404(Post, pk=post_id)
    post.likers.remove(request.user)
    return Status(204, None)


@api.post("/comments/{comment_id}/likes", response={201: None})
def add_comment_like(request: AuthedRequest, comment_id: PositiveInt) -> Status[None]:
    comment = get_object_or_404(Comment, pk=comment_id)
    comment.likers.add(request.user)
    return Status(201, None)


@api.delete("/comments/{comment_id}/likes", response={204: None})
def remove_comment_like(request: AuthedRequest, comment_id: PositiveInt) -> Status[None]:
    comment = get_object_or_404(Comment, pk=comment_id)
    comment.likers.remove(request.user)
    return Status(204, None)


@api.post("/users/{username}/subscriptions", response={201: None})
def add_subscription(request: AuthedRequest, username: str) -> Status[None]:
    to_user = get_object_or_404(User.objects.only("pk"), username=username)
    if to_user.pk == request.user.pk:
        raise HttpError(400, _("You can't subscribe to yourself."))
    request.user.subscriptions.add(to_user)
    return Status(201, None)


@api.delete("/users/{username}/subscriptions", response={204: None})
def remove_subscription(request: AuthedRequest, username: str) -> Status[None]:
    to_user = get_object_or_404(User, username=username)
    request.user.subscriptions.remove(to_user)
    return Status(204, None)
