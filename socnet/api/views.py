from __future__ import annotations

from typing import Any, Dict, Type, Union

from rest_framework import permissions, status, views
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response

from ..blog import models as blog_models
from ..users.exceptions import SelfSubscriptionError
from ..users.models import User
from . import serializers
from .types import AuthedRequest


def validate_pk(data: Union[int, Dict[str, Any]]) -> Any:
    if isinstance(data, int):
        data = {"id": data}
    serializer = serializers.IdSerializer(data=data)
    serializer.is_valid(raise_exception=True)
    return serializer.validated_data["id"]


class _AuthedAPIView(views.APIView):
    permission_classes = (permissions.IsAuthenticated,)


class _UnlikeView(_AuthedAPIView):
    model: Type[Union[blog_models.Post, blog_models.PostComment]]

    def delete(self, request: AuthedRequest, pk: int) -> Response:
        qs = self.model.objects.filter(pk=validate_pk(pk))
        obj = get_object_or_404(qs)
        obj.likers.remove(request.user)  # type: ignore[attr-defined]
        return Response(status=status.HTTP_204_NO_CONTENT)


class _LikeView(_AuthedAPIView):
    model: Type[Union[blog_models.Post, blog_models.PostComment]]

    def post(self, request: AuthedRequest) -> Response:
        qs = self.model.objects.filter(pk=validate_pk(request.data))
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
        qs = User.objects.filter(pk=validate_pk(pk))
        user = get_object_or_404(qs)
        user.subscribers.remove(request.user)
        return Response(status=status.HTTP_204_NO_CONTENT)


class UserSubscribeView(_AuthedAPIView):
    def post(self, request: AuthedRequest) -> Response:
        qs = User.objects.filter(pk=validate_pk(request.data))
        user = get_object_or_404(qs)
        try:
            user.subscribers.add(request.user)
        except SelfSubscriptionError:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        return Response(status=status.HTTP_201_CREATED)
