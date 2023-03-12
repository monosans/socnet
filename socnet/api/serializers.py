from __future__ import annotations

from typing import Any, Dict, Union

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


def validate_pk(data: Any) -> Any:
    if not isinstance(data, dict):
        data = {"pk": data}
    serializer = PkSerializer(data=data)
    serializer.is_valid(raise_exception=True)
    return serializer.validated_data["pk"]


def validate_username(data: Union[str, Dict[str, Any]]) -> Any:
    if not isinstance(data, dict):
        data = {"username": data}
    serializer = UsernameSerializer(data=data)
    serializer.is_valid(raise_exception=True)
    return serializer.validated_data["username"]


class ContentTypeSerializer(serializers.ModelSerializer[ContentType]):
    class Meta:
        model = ContentType
        fields = "__all__"


class EmailAddressSerializer(serializers.ModelSerializer[EmailAddress]):
    class Meta:
        model = EmailAddress
        fields = "__all__"


class GroupSerializer(serializers.ModelSerializer[auth_models.Group]):
    user_set: serializers.RelatedField[User, Any, Any] = serializers.RelatedField(
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
    group_set: serializers.RelatedField[auth_models.Group, Any, Any] = (
        serializers.RelatedField(many=True, read_only=True)
    )
    user_set: serializers.RelatedField[User, Any, Any] = serializers.RelatedField(
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
    liked_comments: serializers.RelatedField[blog_models.Comment, Any, Any] = (
        serializers.RelatedField(many=True, read_only=True)
    )
    liked_posts: serializers.RelatedField[blog_models.Post, Any, Any] = (
        serializers.RelatedField(many=True, read_only=True)
    )
    subscribers: serializers.RelatedField[User, Any, Any] = serializers.RelatedField(
        many=True, read_only=True
    )

    class Meta:
        model = User
        fields = "__all__"
        exclude = ("password",)
