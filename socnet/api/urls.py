from __future__ import annotations

from django.urls import path
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView
from rest_framework import routers

from . import views, viewsets

router = routers.SimpleRouter()
for prefix, viewset in (
    ("content_types", viewsets.ContentTypeViewSet),
    ("email_addresses", viewsets.EmailAddressViewSet),
    ("groups", viewsets.GroupViewSet),
    ("log_entries", viewsets.LogEntryViewSet),
    ("messages", viewsets.MessageViewSet),
    ("permissions", viewsets.PermissionViewSet),
    ("comments", viewsets.CommentViewSet),
    ("posts", viewsets.PostViewSet),
    ("users", viewsets.UserViewSet),
):
    router.register(prefix, viewset)

urlpatterns = [
    *router.urls,
    path("comment_like/<int:pk>/", views.CommentUnlikeView.as_view()),
    path("comment_like/", views.CommentLikeView.as_view()),
    path("post_like/<int:pk>/", views.PostUnlikeView.as_view()),
    path("post_like/", views.PostLikeView.as_view()),
    path("subscription/<str:username>/", views.UserUnsubscribeView.as_view()),
    path("subscription/", views.UserSubscribeView.as_view()),
    path("schema/", SpectacularAPIView.as_view(), name="schema"),
    path("", SpectacularSwaggerView.as_view(url_name="schema"), name="swagger-ui"),
]
