from __future__ import annotations

from typing import Literal

import orjson
from django.core.exceptions import ValidationError
from django.db import IntegrityError
from django.db.models import Subquery
from django.shortcuts import get_object_or_404
from ninja import NinjaAPI, Schema
from ninja.errors import HttpError
from ninja.security import django_auth
from pydantic import PositiveInt

from socnet.blog.models import Comment, Post
from socnet.core.types import AuthedRequest
from socnet.users.models import User

api = NinjaAPI(title="SocNet", csrf=True, auth=django_auth)


class PkSchema(Schema):
    pk: PositiveInt


class UsernameSchema(Schema):
    username: str


@api.post("/post-like", response={201: None})
def add_post_like(
    request: AuthedRequest, payload: PkSchema
) -> tuple[Literal[201], None]:
    post_like = Post.likers.through(post_id=payload.pk, user=request.user)
    try:
        post_like.full_clean()
    except ValidationError as e:
        raise HttpError(400, "\n".join(e.messages))
    post_like.save()
    return 201, None


@api.delete("/post-like", response={204: None})
def remove_post_like(
    request: AuthedRequest, pk: PositiveInt
) -> tuple[Literal[204], None]:
    Post.likers.through.objects.filter(post_id=pk, user=request.user).delete()
    return 204, None


@api.post("/comment-like", response={201: None})
def add_comment_like(
    request: AuthedRequest, payload: PkSchema
) -> tuple[Literal[201], None]:
    comment_like = Comment.likers.through(
        comment_id=payload.pk, user=request.user
    )
    try:
        comment_like.full_clean()
    except ValidationError as e:
        raise HttpError(400, "\n".join(e.messages))
    comment_like.save()
    return 201, None


@api.delete("/comment-like", response={204: None})
def remove_comment_like(
    request: AuthedRequest, pk: PositiveInt
) -> tuple[Literal[204], None]:
    Comment.likers.through.objects.filter(
        comment_id=pk, user=request.user
    ).delete()
    return 204, None


@api.post("/subscription", response={201: None})
def add_subcription(
    request: AuthedRequest, payload: UsernameSchema
) -> tuple[Literal[201], None]:
    to_user = get_object_or_404(
        User.objects.only("pk").filter(username=payload.username)
    )
    subscription = User.subscriptions.through(
        from_user=request.user, to_user=to_user
    )
    try:
        subscription.full_clean()
    except ValidationError as e:
        raise HttpError(400, "\n".join(e.messages))
    subscription.save()
    return 201, None


@api.delete("/subscription", response={204: None})
def remove_subcription(
    request: AuthedRequest, username: str
) -> tuple[Literal[204], None]:
    User.subscriptions.through.objects.filter(
        from_user=request.user,
        to_user=User.objects.filter(username=username)[:1],
    ).delete()
    return 204, None
