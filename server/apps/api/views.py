from typing import Type, Union

from allauth.account.models import EmailAddress
from django.contrib.admin.models import LogEntry
from django.contrib.auth import get_user_model
from django.contrib.auth import models as auth_models
from django.contrib.contenttypes.models import ContentType
from django.db.models import Prefetch
from rest_framework import mixins, permissions, status, views, viewsets
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response

from ..main import models as main_models
from ..messenger import models as messenger_models
from . import serializers
from .types import AuthedRequest

User = get_user_model()


class _AuthedAPIView(views.APIView):
    permission_classes = (permissions.IsAuthenticated,)


class _LikeView(_AuthedAPIView):
    model: Type[Union[main_models.Post, main_models.PostComment]]

    def post(self, request: AuthedRequest) -> Response:
        pk = int(request.data["pk"])
        obj = get_object_or_404(self.model, pk=pk)
        obj.likers.add(request.user)  # type: ignore[attr-defined]
        return Response(status=status.HTTP_201_CREATED)


class _UnlikeView(_AuthedAPIView):
    model: Type[Union[main_models.Post, main_models.PostComment]]

    def delete(self, request: AuthedRequest, pk: int) -> Response:
        obj = get_object_or_404(self.model, pk=pk)
        obj.likers.remove(request.user)  # type: ignore[attr-defined]
        return Response(status=status.HTTP_204_NO_CONTENT)


class PostLikeView(_LikeView):
    model = main_models.Post


class PostUnlikeView(_UnlikeView):
    model = main_models.Post


class PostCommentLikeView(_LikeView):
    model = main_models.PostComment


class PostCommentUnlikeView(_UnlikeView):
    model = main_models.PostComment


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


class ChatViewSet(viewsets.ModelViewSet):
    queryset = messenger_models.Chat.objects.prefetch_related(
        Prefetch("messages", messenger_models.Message.objects.only("chat_id")),
        Prefetch("participants", User.objects.only("pk")),
    )
    serializer_class = serializers.ChatSerializer
    search_fields = ["participants__username"]


class ContentTypeViewSet(viewsets.ModelViewSet):
    queryset = ContentType.objects.all()
    serializer_class = serializers.ContentTypeSerializer


class EmailAddressViewSet(viewsets.ModelViewSet):
    queryset = EmailAddress.objects.only(
        "email", "verified", "primary", "user_id"
    )
    serializer_class = serializers.EmailAddressSerializer
    search_fields = ["email"]


class GroupViewSet(viewsets.ModelViewSet):
    queryset = auth_models.Group.objects.prefetch_related(
        Prefetch("permissions", auth_models.Permission.objects.only("pk"))
    )
    serializer_class = serializers.GroupSerializer
    search_fields = ["name", "permissions__name", "permissions__codename"]


class LogEntryViewSet(
    mixins.RetrieveModelMixin, mixins.ListModelMixin, viewsets.GenericViewSet
):
    queryset = LogEntry.objects.all()
    serializer_class = serializers.LogEntrySerializer
    search_fields = ["user__username"]


class MessageViewSet(viewsets.ModelViewSet):
    queryset = messenger_models.Message.objects.all()
    serializer_class = serializers.MessageSerializer
    search_fields = ["user__username", "text"]


class PermissionViewSet(viewsets.ModelViewSet):
    queryset = auth_models.Permission.objects.all()
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
    ).defer("password")
    serializer_class = serializers.UserSerializer
    search_fields = ["username", "email"]
