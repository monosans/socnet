from __future__ import annotations

from typing import Type, Union

from allauth.account.models import EmailAddress
from django.contrib.admin.models import LogEntry
from django.contrib.auth import models as auth_models
from django.contrib.contenttypes.models import ContentType
from django.db.models import Prefetch
from drf_spectacular.utils import extend_schema
from rest_framework import permissions, status, viewsets
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet

from ..blog import models as blog_models
from ..messenger import models as messenger_models
from ..users.exceptions import SelfSubscriptionError
from ..users.models import User
from . import filters, serializers
from .types import AuthedRequest


class _AuthedViewSet(ViewSet):
    permission_classes = (permissions.IsAuthenticated,)


class _LikeViewSet(_AuthedViewSet):
    model: Type[Union[blog_models.Post, blog_models.Comment]]
    serializer_class = serializers.PkSerializer

    @extend_schema(responses=None)
    def create(self, request: AuthedRequest) -> Response:
        pk = serializers.validate_single_field(
            self.serializer_class, "pk", request.data
        )
        qs = self.model.objects.filter(pk=pk)
        obj = get_object_or_404(qs)
        obj.likers.add(request.user)  # type: ignore[attr-defined]
        return Response(status=status.HTTP_201_CREATED)

    def destroy(self, request: AuthedRequest, pk: int) -> Response:
        valid_pk = serializers.validate_single_field(self.serializer_class, "pk", pk)
        qs = self.model.objects.filter(pk=valid_pk)
        obj = get_object_or_404(qs)
        obj.likers.remove(request.user)  # type: ignore[attr-defined]
        return Response(status=status.HTTP_204_NO_CONTENT)


class PostLikeViewSet(_LikeViewSet):
    model = blog_models.Post


class CommentLikeViewSet(_LikeViewSet):
    model = blog_models.Comment


class SubscriptionViewSet(_AuthedViewSet):
    lookup_field = "username"
    serializer_class = serializers.UsernameSerializer

    @extend_schema(responses=None)
    def create(self, request: AuthedRequest) -> Response:
        username = serializers.validate_single_field(
            self.serializer_class, self.lookup_field, request.data
        )
        qs = User.objects.filter(username=username)
        user = get_object_or_404(qs)
        try:
            user.subscribers.add(request.user)
        except SelfSubscriptionError:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        return Response(status=status.HTTP_201_CREATED)

    def destroy(self, request: AuthedRequest, username: str) -> Response:
        valid_username = serializers.validate_single_field(
            self.serializer_class, self.lookup_field, username
        )
        qs = User.objects.filter(username=valid_username)
        user = get_object_or_404(qs)
        user.subscribers.remove(request.user)
        return Response(status=status.HTTP_204_NO_CONTENT)


class ContentTypeViewSet(viewsets.ReadOnlyModelViewSet[ContentType]):
    queryset = ContentType.objects.all()
    serializer_class = serializers.ContentTypeSerializer
    filterset_class = filters.generate_filterset(serializer_class)


class EmailAddressViewSet(viewsets.ModelViewSet[EmailAddress]):
    queryset = EmailAddress.objects.all()
    serializer_class = serializers.EmailAddressSerializer
    filterset_class = filters.generate_filterset(serializer_class)


class GroupViewSet(viewsets.ModelViewSet[auth_models.Group]):
    queryset = auth_models.Group.objects.prefetch_related(
        Prefetch("permissions", auth_models.Permission.objects.only("pk")),
        Prefetch("user_set", User.objects.only("pk")),
    )
    serializer_class = serializers.GroupSerializer
    filterset_class = filters.generate_filterset(serializer_class)


class LogEntryViewSet(viewsets.ReadOnlyModelViewSet[LogEntry]):
    queryset = LogEntry.objects.all()
    serializer_class = serializers.LogEntrySerializer
    filterset_class = filters.generate_filterset(serializer_class)


class MessageViewSet(viewsets.ModelViewSet[messenger_models.Message]):
    queryset = messenger_models.Message.objects.all()
    serializer_class = serializers.MessageSerializer
    filterset_class = filters.generate_filterset(serializer_class)


class PermissionViewSet(viewsets.ReadOnlyModelViewSet[auth_models.Permission]):
    queryset = auth_models.Permission.objects.prefetch_related(
        Prefetch("group_set", auth_models.Group.objects.only("pk")),
        Prefetch("user_set", User.objects.only("pk")),
    )
    serializer_class = serializers.PermissionSerializer
    filterset_class = filters.generate_filterset(serializer_class)


class CommentViewSet(viewsets.ModelViewSet[blog_models.Comment]):
    queryset = blog_models.Comment.objects.prefetch_related(
        Prefetch("likers", User.objects.only("pk"))
    )
    serializer_class = serializers.CommentSerializer
    filterset_class = filters.generate_filterset(serializer_class)


class PostViewSet(viewsets.ModelViewSet[blog_models.Post]):
    queryset = blog_models.Post.objects.prefetch_related(
        Prefetch("likers", User.objects.only("pk"))
    )
    serializer_class = serializers.PostSerializer
    filterset_class = filters.generate_filterset(serializer_class)


class UserViewSet(viewsets.ModelViewSet[User]):
    queryset = User.objects.defer("password").prefetch_related(
        Prefetch("groups", auth_models.Group.objects.only("pk")),
        Prefetch("liked_comments", blog_models.Comment.objects.only("pk")),
        Prefetch("liked_posts", blog_models.Post.objects.only("pk")),
        Prefetch("subscribers", User.objects.only("pk")),
        Prefetch("subscriptions", User.objects.only("pk")),
        Prefetch("user_permissions", auth_models.Permission.objects.only("pk")),
    )
    serializer_class = serializers.UserSerializer
    filterset_class = filters.generate_filterset(serializer_class)
