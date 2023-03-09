from __future__ import annotations

from typing import Any

from allauth.account.models import EmailAddress
from django.contrib.admin.models import LogEntry
from django.contrib.auth import models as auth_models
from django.contrib.contenttypes.models import ContentType
from rest_framework import serializers

from ..blog import models as blog_models
from ..messenger import models as messenger_models
from ..users.models import User


class PkSerializer(serializers.Serializer[Any]):
    pk = serializers.IntegerField(min_value=1)


class UsernameSerializer(serializers.Serializer[Any]):
    username = serializers.CharField(min_length=1)


class ContentTypeSerializer(serializers.HyperlinkedModelSerializer):
    logentry_set: serializers.HyperlinkedRelatedField[LogEntry] = (
        serializers.HyperlinkedRelatedField(
            many=True, read_only=True, view_name="logentry-detail"
        )
    )
    permission_set: serializers.HyperlinkedRelatedField[auth_models.Permission] = (
        serializers.HyperlinkedRelatedField(
            many=True, read_only=True, view_name="permission-detail"
        )
    )

    class Meta:
        model = ContentType
        fields = "__all__"


class EmailAddressSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = EmailAddress
        fields = "__all__"


class GroupSerializer(serializers.HyperlinkedModelSerializer):
    user_set: serializers.HyperlinkedRelatedField[User] = (
        serializers.HyperlinkedRelatedField(
            many=True, read_only=True, view_name="user-detail"
        )
    )

    class Meta:
        model = auth_models.Group
        fields = "__all__"


class LogEntrySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = LogEntry
        fields = "__all__"


class MessageSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = messenger_models.Message
        fields = "__all__"


class PermissionSerializer(serializers.HyperlinkedModelSerializer):
    group_set: serializers.HyperlinkedRelatedField[auth_models.Group] = (
        serializers.HyperlinkedRelatedField(
            many=True, read_only=True, view_name="group-detail"
        )
    )
    user_set: serializers.HyperlinkedRelatedField[User] = (
        serializers.HyperlinkedRelatedField(
            many=True, read_only=True, view_name="user-detail"
        )
    )

    class Meta:
        model = auth_models.Permission
        fields = "__all__"


class CommentSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = blog_models.Comment
        fields = "__all__"


class PostSerializer(serializers.HyperlinkedModelSerializer):
    comments: serializers.HyperlinkedRelatedField[blog_models.Comment] = (
        serializers.HyperlinkedRelatedField(
            many=True, read_only=True, view_name="comment-detail"
        )
    )

    class Meta:
        model = blog_models.Post
        fields = "__all__"


class UserSerializer(serializers.HyperlinkedModelSerializer):
    emailaddress_set: serializers.HyperlinkedRelatedField[EmailAddress] = (
        serializers.HyperlinkedRelatedField(
            many=True, read_only=True, view_name="emailaddress-detail"
        )
    )
    liked_comments: serializers.HyperlinkedRelatedField[blog_models.Comment] = (
        serializers.HyperlinkedRelatedField(
            many=True, read_only=True, view_name="comment-detail"
        )
    )
    liked_posts: serializers.HyperlinkedRelatedField[blog_models.Post] = (
        serializers.HyperlinkedRelatedField(
            many=True, read_only=True, view_name="post-detail"
        )
    )
    logentry_set: serializers.HyperlinkedRelatedField[LogEntry] = (
        serializers.HyperlinkedRelatedField(
            many=True, read_only=True, view_name="logentry-detail"
        )
    )
    outgoing_messages: serializers.HyperlinkedRelatedField[messenger_models.Message] = (
        serializers.HyperlinkedRelatedField(
            many=True, read_only=True, view_name="message-detail"
        )
    )
    comments: serializers.HyperlinkedRelatedField[blog_models.Comment] = (
        serializers.HyperlinkedRelatedField(
            many=True, read_only=True, view_name="comment-detail"
        )
    )
    posts: serializers.HyperlinkedRelatedField[blog_models.Post] = (
        serializers.HyperlinkedRelatedField(
            many=True, read_only=True, view_name="post-detail"
        )
    )
    subscribers: serializers.HyperlinkedRelatedField[User] = (
        serializers.HyperlinkedRelatedField(
            many=True, read_only=True, view_name="user-detail"
        )
    )

    class Meta:
        model = User
        fields = "__all__"
