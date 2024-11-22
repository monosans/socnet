from __future__ import annotations

from typing import Any

from allauth.account.models import EmailAddress
from django.contrib.admin.models import LogEntry
from django.contrib.auth import models as auth_models
from django.contrib.contenttypes.models import ContentType
from rest_framework import serializers

from socnet.blog import models as blog_models
from socnet.messenger import models as messenger_models
from socnet.users.models import User


class PkSerializer(serializers.Serializer[Any]):
    pk = serializers.IntegerField(min_value=1)


class UsernameSerializer(serializers.Serializer[Any]):
    username = serializers.CharField(min_length=1)


def validate_single_field(
    serializer_cls: type[serializers.Serializer[Any]], field: str, data: Any
) -> Any:
    if not isinstance(data, dict):
        data = {field: data}
    serializer = serializer_cls(data=data)
    serializer.is_valid(raise_exception=True)
    return serializer.validated_data[field]


class ContentTypeSerializer(serializers.ModelSerializer[ContentType]):
    class Meta:
        model = ContentType
        fields = "__all__"


class EmailAddressSerializer(serializers.ModelSerializer[EmailAddress]):
    class Meta:
        model = EmailAddress
        fields = "__all__"


class GroupSerializer(serializers.ModelSerializer[auth_models.Group]):
    user_set = serializers.PrimaryKeyRelatedField[User](
        many=True, read_only=True
    )

    class Meta:
        model = auth_models.Group
        fields = "__all__"


class LogEntrySerializer(serializers.ModelSerializer[LogEntry]):
    class Meta:
        model = LogEntry
        fields = "__all__"


class MessageSerializer(serializers.ModelSerializer[messenger_models.Message]):
    class Meta:
        model = messenger_models.Message
        fields = "__all__"


class PermissionSerializer(serializers.ModelSerializer[auth_models.Permission]):
    group_set = serializers.PrimaryKeyRelatedField[auth_models.Group](
        many=True, read_only=True
    )
    user_set = serializers.PrimaryKeyRelatedField[User](
        many=True, read_only=True
    )

    class Meta:
        model = auth_models.Permission
        fields = "__all__"


class CommentSerializer(serializers.ModelSerializer[blog_models.Comment]):
    class Meta:
        model = blog_models.Comment
        fields = "__all__"


class PostSerializer(serializers.ModelSerializer[blog_models.Post]):
    class Meta:
        model = blog_models.Post
        fields = "__all__"


class UserSerializer(serializers.ModelSerializer[User]):
    liked_comments = serializers.PrimaryKeyRelatedField[blog_models.Comment](
        many=True, read_only=True
    )
    liked_posts = serializers.PrimaryKeyRelatedField[blog_models.Post](
        many=True, read_only=True
    )
    subscribers = serializers.PrimaryKeyRelatedField[User](
        many=True, read_only=True
    )

    class Meta:
        model = User
        exclude = ("password",)
