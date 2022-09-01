from __future__ import annotations

from django.urls import path
from rest_framework import routers

from . import views, viewsets

router = routers.DefaultRouter()
router.register("chats", viewsets.ChatViewSet)
router.register("content_types", viewsets.ContentTypeViewSet)
router.register("email_addresses", viewsets.EmailAddressViewSet)
router.register("groups", viewsets.GroupViewSet)
router.register("log_entries", viewsets.LogEntryViewSet)
router.register("messages", viewsets.MessageViewSet)
router.register("permissions", viewsets.PermissionViewSet)
router.register("post_comments", viewsets.PostCommentViewSet)
router.register("posts", viewsets.PostViewSet)
router.register("users", viewsets.UserViewSet)

urlpatterns = [
    *router.urls,
    path(
        "post_comment_like/<int:pk>/",
        views.PostCommentUnlikeView.as_view(),
        name="post_comment_unlike",
    ),
    path(
        "post_comment_like/",
        views.PostCommentLikeView.as_view(),
        name="post_comment_like",
    ),
    path(
        "post_like/<int:pk>/",
        views.PostUnlikeView.as_view(),
        name="post_unlike",
    ),
    path("post_like/", views.PostLikeView.as_view(), name="post_like"),
    path(
        "subscription/<int:pk>/",
        views.UserUnsubscribeView.as_view(),
        name="user_unsubscribe",
    ),
    path(
        "subscription/",
        views.UserSubscribeView.as_view(),
        name="user_subscribe",
    ),
]
