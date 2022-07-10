from __future__ import annotations

from django.urls import include, path
from rest_framework import routers

from . import views

router = routers.DefaultRouter()
router.register("chats", views.ChatViewSet)
router.register("content_types", views.ContentTypeViewSet)
router.register("email_addresses", views.EmailAddressViewSet)
router.register("groups", views.GroupViewSet)
router.register("log_entries", views.LogEntryViewSet)
router.register("messages", views.MessageViewSet)
router.register("permissions", views.PermissionViewSet)
router.register("post_comments", views.PostCommentViewSet)
router.register("posts", views.PostViewSet)
router.register("users", views.UserViewSet)

urlpatterns = [
    path("", include(router.urls)),
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
