from __future__ import annotations

from allauth.account.models import EmailAddress
from django.contrib.admin.models import LogEntry
from django.contrib.auth import get_user_model
from django.contrib.auth import models as auth_models
from django.contrib.contenttypes.models import ContentType
from django.db.models import Prefetch
from rest_framework import viewsets

from ..main import models as main_models
from ..messenger import models as messenger_models
from . import serializers

User = get_user_model()

# pylint: disable=too-many-ancestors
class ChatViewSet(viewsets.ModelViewSet):
    queryset = messenger_models.Chat.objects.prefetch_related(
        Prefetch("messages", messenger_models.Message.objects.only("chat_id")),
        Prefetch("participants", User.objects.only("pk")),
    )
    serializer_class = serializers.ChatSerializer
    search_fields = ["participants__username"]


class ContentTypeViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = ContentType.objects.prefetch_related(
        Prefetch("logentry_set", LogEntry.objects.only("content_type_id")),
        Prefetch(
            "permission_set",
            auth_models.Permission.objects.only("content_type_id"),
        ),
    )
    serializer_class = serializers.ContentTypeSerializer


class EmailAddressViewSet(viewsets.ModelViewSet):
    queryset = EmailAddress.objects.all()
    serializer_class = serializers.EmailAddressSerializer
    search_fields = ["email"]


class GroupViewSet(viewsets.ModelViewSet):
    queryset = auth_models.Group.objects.prefetch_related(
        Prefetch("permissions", auth_models.Permission.objects.only("pk")),
        Prefetch("user_set", User.objects.only("pk")),
    )
    serializer_class = serializers.GroupSerializer
    search_fields = ["name", "permissions__name", "permissions__codename"]


class LogEntryViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = LogEntry.objects.all()
    serializer_class = serializers.LogEntrySerializer
    search_fields = ["user__username"]


class MessageViewSet(viewsets.ModelViewSet):
    queryset = messenger_models.Message.objects.all()
    serializer_class = serializers.MessageSerializer
    search_fields = ["user__username", "text"]


class PermissionViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = auth_models.Permission.objects.prefetch_related(
        Prefetch("group_set", auth_models.Group.objects.only("pk")),
        Prefetch("user_set", User.objects.only("pk")),
    )
    serializer_class = serializers.PermissionSerializer
    search_fields = ["name", "codename"]


class PostCommentViewSet(viewsets.ModelViewSet):
    queryset = main_models.PostComment.objects.prefetch_related(
        Prefetch("likers", User.objects.only("pk"))
    )
    serializer_class = serializers.PostCommentSerializer
    search_fields = ["user__username", "text"]


class PostViewSet(viewsets.ModelViewSet):
    queryset = main_models.Post.objects.prefetch_related(
        Prefetch("comments", main_models.PostComment.objects.only("post_id")),
        Prefetch("likers", User.objects.only("pk")),
    )
    serializer_class = serializers.PostSerializer
    search_fields = ["user__username", "text"]


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.prefetch_related(
        Prefetch("chats", messenger_models.Chat.objects.only("pk")),
        Prefetch("emailaddress_set", EmailAddress.objects.only("user_id")),
        Prefetch(
            "liked_comments", main_models.PostComment.objects.only("user_id")
        ),
        Prefetch("liked_posts", main_models.Post.objects.only("pk")),
        Prefetch("logentry_set", LogEntry.objects.only("user_id")),
        Prefetch(
            "outgoing_messages",
            messenger_models.Message.objects.only("user_id"),
        ),
        Prefetch(
            "post_comments", main_models.PostComment.objects.only("user_id")
        ),
        Prefetch("posts", main_models.Post.objects.only("user_id")),
        Prefetch("subscribers", User.objects.only("pk")),
        Prefetch("groups", auth_models.Group.objects.only("pk")),
        Prefetch(
            "user_permissions", auth_models.Permission.objects.only("pk")
        ),
        Prefetch("subscriptions", User.objects.only("pk")),
    )
    serializer_class = serializers.UserSerializer
    search_fields = ["username", "email"]
