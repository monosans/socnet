from django.urls import include, path
from rest_framework import routers
from rest_framework import urls as drf_urls

from . import views

router = routers.DefaultRouter()
router.register("access_attempts", views.AccessAttemptViewset)
router.register("chats", views.ChatViewset)
router.register("content_types", views.ContentTypeViewset)
router.register("groups", views.GroupViewset)
router.register("log_entries", views.LogEntryViewset)
router.register("messages", views.MessageViewset)
router.register("permissions", views.PermissionViewset)
router.register("post_comments", views.PostCommentViewset)
router.register("posts", views.PostViewset)
router.register("users", views.UserViewset)

urlpatterns = [
    path("", include(router.urls)),
    path("api-auth/", include(drf_urls)),
    path(
        "like_post_comment/<int:pk>/",
        views.UnlikePostComment.as_view(),
        name="unlike_post_comment",
    ),
    path(
        "like_post_comment/",
        views.LikePostComment.as_view(),
        name="like_post_comment",
    ),
    path(
        "like_post/<int:pk>/", views.UnlikePost.as_view(), name="unlike_post"
    ),
    path("like_post/", views.LikePost.as_view(), name="like_post"),
    path(
        "subscription/<int:pk>/",
        views.Unsubscribe.as_view(),
        name="unsubscribe",
    ),
    path("subscription/", views.Subscribe.as_view(), name="subscribe"),
]
