from allauth.account.models import EmailAddress
from django.contrib.admin.models import LogEntry
from django.contrib.auth import get_user_model
from django.contrib.auth import models as auth_models
from django.contrib.contenttypes.models import ContentType
from rest_framework import serializers

from ..main import models as main_models
from ..messenger import models as messenger_models
from ..users.models import User as UserType

User = get_user_model()


class ChatSerializer(serializers.HyperlinkedModelSerializer):
    messages: serializers.HyperlinkedRelatedField[
        messenger_models.Message
    ] = serializers.HyperlinkedRelatedField(
        many=True, read_only=True, view_name="message-detail"
    )

    class Meta:
        model = messenger_models.Chat
        fields = "__all__"


class ContentTypeSerializer(serializers.HyperlinkedModelSerializer):
    logentry_set: serializers.HyperlinkedRelatedField[
        LogEntry
    ] = serializers.HyperlinkedRelatedField(
        many=True, read_only=True, view_name="logentry-detail"
    )
    permission_set: serializers.HyperlinkedRelatedField[
        auth_models.Permission
    ] = serializers.HyperlinkedRelatedField(
        many=True, read_only=True, view_name="permission-detail"
    )

    class Meta:
        model = ContentType
        fields = "__all__"


class EmailAddressSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = EmailAddress
        fields = "__all__"


class GroupSerializer(serializers.HyperlinkedModelSerializer):
    user_set: serializers.HyperlinkedRelatedField[
        UserType
    ] = serializers.HyperlinkedRelatedField(
        many=True, read_only=True, view_name="user-detail"
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
    group_set: serializers.HyperlinkedRelatedField[
        auth_models.Group
    ] = serializers.HyperlinkedRelatedField(
        many=True, read_only=True, view_name="group-detail"
    )
    user_set: serializers.HyperlinkedRelatedField[
        UserType
    ] = serializers.HyperlinkedRelatedField(
        many=True, read_only=True, view_name="user-detail"
    )

    class Meta:
        model = auth_models.Permission
        fields = "__all__"


class PostCommentSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = main_models.PostComment
        fields = "__all__"


class PostSerializer(serializers.HyperlinkedModelSerializer):
    comments: serializers.HyperlinkedRelatedField[
        main_models.PostComment
    ] = serializers.HyperlinkedRelatedField(
        many=True, read_only=True, view_name="postcomment-detail"
    )

    class Meta:
        model = main_models.Post
        fields = "__all__"


class UserSerializer(serializers.HyperlinkedModelSerializer):
    chats: serializers.HyperlinkedRelatedField[
        messenger_models.Chat
    ] = serializers.HyperlinkedRelatedField(
        many=True, read_only=True, view_name="chat-detail"
    )
    emailaddress_set: serializers.HyperlinkedRelatedField[
        EmailAddress
    ] = serializers.HyperlinkedRelatedField(
        many=True, read_only=True, view_name="emailaddress-detail"
    )
    liked_comments: serializers.HyperlinkedRelatedField[
        main_models.PostComment
    ] = serializers.HyperlinkedRelatedField(
        many=True, read_only=True, view_name="postcomment-detail"
    )
    liked_posts: serializers.HyperlinkedRelatedField[
        main_models.Post
    ] = serializers.HyperlinkedRelatedField(
        many=True, read_only=True, view_name="post-detail"
    )
    logentry_set: serializers.HyperlinkedRelatedField[
        LogEntry
    ] = serializers.HyperlinkedRelatedField(
        many=True, read_only=True, view_name="logentry-detail"
    )
    outgoing_messages: serializers.HyperlinkedRelatedField[
        messenger_models.Message
    ] = serializers.HyperlinkedRelatedField(
        many=True, read_only=True, view_name="message-detail"
    )
    post_comments: serializers.HyperlinkedRelatedField[
        main_models.PostComment
    ] = serializers.HyperlinkedRelatedField(
        many=True, read_only=True, view_name="postcomment-detail"
    )
    posts: serializers.HyperlinkedRelatedField[
        main_models.Post
    ] = serializers.HyperlinkedRelatedField(
        many=True, read_only=True, view_name="post-detail"
    )
    subscribers: serializers.HyperlinkedRelatedField[
        UserType
    ] = serializers.HyperlinkedRelatedField(
        many=True, read_only=True, view_name="user-detail"
    )

    class Meta:
        model = User
        exclude = ["password"]
        read_only_fields = ["date_joined", "last_login"]
