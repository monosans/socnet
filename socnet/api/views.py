from __future__ import annotations

from typing import Type, Union

from django.contrib.auth import get_user_model
from rest_framework import permissions, status, views
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response

from ..blog import models as blog_models
from ..users.models import User as UserType
from .types import AuthedRequest

User: Type[UserType] = get_user_model()


class _AuthedAPIView(views.APIView):
    permission_classes = (permissions.IsAuthenticated,)


class _LikeView(_AuthedAPIView):
    model: Type[Union[blog_models.Post, blog_models.PostComment]]

    def post(self, request: AuthedRequest) -> Response:
        pk = int(request.data["pk"])
        obj = get_object_or_404(self.model, pk=pk)
        obj.likers.add(request.user)  # type: ignore[attr-defined]
        return Response(status=status.HTTP_201_CREATED)


class _UnlikeView(_AuthedAPIView):
    model: Type[Union[blog_models.Post, blog_models.PostComment]]

    def delete(self, request: AuthedRequest, pk: int) -> Response:
        obj = get_object_or_404(self.model, pk=pk)
        obj.likers.remove(request.user)  # type: ignore[attr-defined]
        return Response(status=status.HTTP_204_NO_CONTENT)


class PostLikeView(_LikeView):
    model = blog_models.Post


class PostUnlikeView(_UnlikeView):
    model = blog_models.Post


class PostCommentLikeView(_LikeView):
    model = blog_models.PostComment


class PostCommentUnlikeView(_UnlikeView):
    model = blog_models.PostComment


class UserSubscribeView(_AuthedAPIView):
    def post(self, request: AuthedRequest) -> Response:
        pk = int(request.data["pk"])
        user = get_object_or_404(User, pk=pk)
        user.subscribers.add(request.user)
        return Response(status=status.HTTP_201_CREATED)


class UserUnsubscribeView(_AuthedAPIView):
    def delete(self, request: AuthedRequest, pk: int) -> Response:
        user = get_object_or_404(User, pk=pk)
        user.subscribers.remove(request.user)
        return Response(status=status.HTTP_204_NO_CONTENT)
