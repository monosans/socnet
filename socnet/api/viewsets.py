from __future__ import annotations

from typing import Type, Union

from allauth.account.models import EmailAddress
from django.contrib.admin.models import LogEntry
from django.contrib.auth import models as auth_models
from django.contrib.contenttypes.models import ContentType
from django.db.models import Prefetch
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

    def create(self, request: AuthedRequest) -> Response:
        qs = self.model.objects.filter(pk=serializers.validate_pk(request.data))
        obj = get_object_or_404(qs)
        obj.likers.add(request.user)  # type: ignore[attr-defined]
        return Response(status=status.HTTP_201_CREATED)

    def destroy(self, request: AuthedRequest, pk: str) -> Response:
        qs = self.model.objects.filter(pk=serializers.validate_pk(pk))
        obj = get_object_or_404(qs)
        obj.likers.remove(request.user)  # type: ignore[attr-defined]
        return Response(status=status.HTTP_204_NO_CONTENT)


class PostLikeViewSet(_LikeViewSet):
    model = blog_models.Post


class CommentLikeViewSet(_LikeViewSet):
    model = blog_models.Comment


class SubscriptionViewSet(_AuthedViewSet):
    lookup_field = "username"

    def create(self, request: AuthedRequest) -> Response:
        qs = User.objects.filter(username=serializers.validate_username(request.data))
        user = get_object_or_404(qs)
        try:
            user.subscribers.add(request.user)
        except SelfSubscriptionError:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        return Response(status=status.HTTP_201_CREATED)

    def destroy(self, request: AuthedRequest, username: str) -> Response:
        qs = User.objects.filter(username=serializers.validate_username(username))
        user = get_object_or_404(qs)
        user.subscribers.remove(request.user)
        return Response(status=status.HTTP_204_NO_CONTENT)


class ContentTypeViewSet(viewsets.ReadOnlyModelViewSet[ContentType]):
    queryset = ContentType.objects.prefetch_related(
        Prefetch("logentry_set", LogEntry.objects.only("content_type_id")),
        Prefetch(
            "permission_set", auth_models.Permission.objects.only("content_type_id")
        ),
    )
    serializer_class = serializers.ContentTypeSerializer
    filterset_class = filters.ContentTypeFilter


class EmailAddressViewSet(viewsets.ModelViewSet[EmailAddress]):
    queryset = EmailAddress.objects.all()
    serializer_class = serializers.EmailAddressSerializer
    filterset_class = filters.EmailAddressFilter


class GroupViewSet(viewsets.ModelViewSet[auth_models.Group]):
    queryset = auth_models.Group.objects.prefetch_related(
        Prefetch("permissions", auth_models.Permission.objects.only("pk")),
        Prefetch("user_set", User.objects.only("pk")),
    )
    serializer_class = serializers.GroupSerializer
    filterset_class = filters.GroupFilter


class LogEntryViewSet(viewsets.ReadOnlyModelViewSet[LogEntry]):
    queryset = LogEntry.objects.all()
    serializer_class = serializers.LogEntrySerializer
    filterset_class = filters.LogEntryFilter


class MessageViewSet(viewsets.ModelViewSet[messenger_models.Message]):
    queryset = messenger_models.Message.objects.all()
    serializer_class = serializers.MessageSerializer
    filterset_class = filters.MessageFilter


class PermissionViewSet(viewsets.ReadOnlyModelViewSet[auth_models.Permission]):
    queryset = auth_models.Permission.objects.prefetch_related(
        Prefetch("group_set", auth_models.Group.objects.only("pk")),
        Prefetch("user_set", User.objects.only("pk")),
    )
    serializer_class = serializers.PermissionSerializer
    filterset_class = filters.PermissionFilter


class CommentViewSet(viewsets.ModelViewSet[blog_models.Comment]):
    queryset = blog_models.Comment.objects.prefetch_related(
        Prefetch("likers", User.objects.only("pk"))
    )
    serializer_class = serializers.CommentSerializer
    filterset_class = filters.CommentFilter


class PostViewSet(viewsets.ModelViewSet[blog_models.Post]):
    queryset = blog_models.Post.objects.prefetch_related(
        Prefetch("comments", blog_models.Comment.objects.only("post_id")),
        Prefetch("likers", User.objects.only("pk")),
    )
    serializer_class = serializers.PostSerializer
    filterset_class = filters.PostFilter


class UserViewSet(viewsets.ModelViewSet[User]):
    queryset = User.objects.prefetch_related(
        Prefetch("emailaddress_set", EmailAddress.objects.only("user_id")),
        Prefetch("liked_comments", blog_models.Comment.objects.only("user_id")),
        Prefetch("liked_posts", blog_models.Post.objects.only("pk")),
        Prefetch("logentry_set", LogEntry.objects.only("user_id")),
        Prefetch(
            "outgoing_messages", messenger_models.Message.objects.only("sender_id")
        ),
        Prefetch("comments", blog_models.Comment.objects.only("author_id")),
        Prefetch("posts", blog_models.Post.objects.only("author_id")),
        Prefetch("subscribers", User.objects.only("pk")),
        Prefetch("groups", auth_models.Group.objects.only("pk")),
        Prefetch("user_permissions", auth_models.Permission.objects.only("pk")),
        Prefetch("subscriptions", User.objects.only("pk")),
    )
    serializer_class = serializers.UserSerializer
    filterset_class = filters.UserFilter
