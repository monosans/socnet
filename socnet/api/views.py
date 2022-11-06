from __future__ import annotations

from typing import Type, Union

from rest_framework import permissions, status, views
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response

from ..blog import models as blog_models
from ..users.exceptions import SelfSubscriptionError
from ..users.models import User
from .types import AuthedRequest


class _AuthedAPIView(views.APIView):
    permission_classes = (permissions.IsAuthenticated,)


class _UnlikeView(_AuthedAPIView):
    model: Type[Union[blog_models.Post, blog_models.PostComment]]

    def delete(self, request: AuthedRequest, pk: int) -> Response:
        qs = self.model.objects.filter(pk=pk)
        obj = get_object_or_404(qs)
        obj.likers.remove(request.user)  # type: ignore[attr-defined]
        return Response(status=status.HTTP_204_NO_CONTENT)


class _LikeView(_AuthedAPIView):
    model: Type[Union[blog_models.Post, blog_models.PostComment]]

    def post(self, request: AuthedRequest) -> Response:
        pk = int(request.data["pk"])
        qs = self.model.objects.filter(pk=pk)
        obj = get_object_or_404(qs)
        obj.likers.add(request.user)  # type: ignore[attr-defined]
        return Response(status=status.HTTP_201_CREATED)


class PostUnlikeView(_UnlikeView):
    model = blog_models.Post


class PostLikeView(_LikeView):
    model = blog_models.Post


class PostCommentUnlikeView(_UnlikeView):
    model = blog_models.PostComment


class PostCommentLikeView(_LikeView):
    model = blog_models.PostComment


class UserUnsubscribeView(_AuthedAPIView):
    def delete(self, request: AuthedRequest, pk: int) -> Response:
        qs = User.objects.filter(pk=pk)
        user = get_object_or_404(qs)
        user.subscribers.remove(request.user)
        return Response(status=status.HTTP_204_NO_CONTENT)


class UserSubscribeView(_AuthedAPIView):
    def post(self, request: AuthedRequest) -> Response:
        pk = int(request.data["pk"])
        qs = User.objects.filter(pk=pk)
        user = get_object_or_404(qs)
        try:
            user.subscribers.add(request.user)
        except SelfSubscriptionError:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        return Response(status=status.HTTP_201_CREATED)
