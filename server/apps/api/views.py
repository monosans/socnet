from typing import Type, Union

from defender.models import AccessAttempt
from django.contrib.admin.models import LogEntry
from django.contrib.auth import get_user_model
from django.contrib.auth import models as auth_models
from django.contrib.contenttypes.models import ContentType
from django_auto_prefetching import AutoPrefetchViewSetMixin
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


class _Like(_AuthedAPIView):
    model: Type[Union[main_models.Post, main_models.PostComment]]

    def post(self, request: AuthedRequest) -> Response:
        obj = get_object_or_404(self.model, pk=request.data["pk"])
        obj.likers.add(request.user)  # type: ignore[attr-defined]
        return Response(status=status.HTTP_201_CREATED)


class _Unlike(_AuthedAPIView):
    model: Type[Union[main_models.Post, main_models.PostComment]]

    def delete(self, request: AuthedRequest, pk: int) -> Response:
        obj = get_object_or_404(self.model, pk=pk)
        obj.likers.remove(request.user)  # type: ignore[attr-defined]
        return Response(status=status.HTTP_204_NO_CONTENT)


class LikePost(_Like):
    model = main_models.Post


class UnlikePost(_Unlike):
    model = main_models.Post


class LikePostComment(_Like):
    model = main_models.PostComment


class UnlikePostComment(_Unlike):
    model = main_models.PostComment


class Subscribe(_AuthedAPIView):
    def post(self, request: AuthedRequest) -> Response:
        user = get_object_or_404(User, pk=request.data["pk"])
        user.subscribers.add(request.user)  # type: ignore[attr-defined]
        return Response(status=status.HTTP_201_CREATED)


class Unsubscribe(_AuthedAPIView):
    def delete(self, request: AuthedRequest, pk: int) -> Response:
        user = get_object_or_404(User, pk=pk)
        user.subscribers.remove(request.user)  # type: ignore[attr-defined]
        return Response(status=status.HTTP_204_NO_CONTENT)


class AutoPrefetchModelViewSet(
    AutoPrefetchViewSetMixin, viewsets.ModelViewSet  # type: ignore[misc]
):
    pass


class MessageViewset(AutoPrefetchModelViewSet):
    queryset = messenger_models.Message.objects.all()
    serializer_class = serializers.MessageSerializer


class UserViewset(AutoPrefetchModelViewSet):
    queryset = User.objects.all()
    serializer_class = serializers.UserSerializer


class PostCommentViewset(AutoPrefetchModelViewSet):
    queryset = main_models.PostComment.objects.all()
    serializer_class = serializers.PostCommentSerializer


class PostViewset(AutoPrefetchModelViewSet):
    queryset = main_models.Post.objects.all()
    serializer_class = serializers.PostSerializer


class ChatViewset(AutoPrefetchModelViewSet):
    queryset = messenger_models.Chat.objects.all()
    serializer_class = serializers.ChatSerializer


class GroupViewset(AutoPrefetchModelViewSet):
    queryset = auth_models.Group.objects.all()
    serializer_class = serializers.GroupSerializer


class AccessAttemptViewset(AutoPrefetchModelViewSet):
    queryset = AccessAttempt.objects.all()
    serializer_class = serializers.AccessAttemptSerializer


class PermissionViewset(AutoPrefetchModelViewSet):
    queryset = auth_models.Permission.objects.all()
    serializer_class = serializers.PermissionSerializer


class LogEntryViewset(
    AutoPrefetchViewSetMixin,  # type: ignore[misc]
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.ListModelMixin,
    viewsets.GenericViewSet,
):
    queryset = LogEntry.objects.all()
    serializer_class = serializers.LogEntrySerializer


class ContentTypeViewset(AutoPrefetchModelViewSet):
    queryset = ContentType.objects.all()
    serializer_class = serializers.ContentTypeSerializer
