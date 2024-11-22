from __future__ import annotations

from django.urls import path
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView
from rest_framework import routers

from socnet.api import viewsets

router = routers.SimpleRouter()
for prefix, viewset, basename in (
    ("comment-likes", viewsets.CommentLikeViewSet, "comment_likes"),
    ("post-likes", viewsets.PostLikeViewSet, "post_likes"),
    ("subscriptions", viewsets.SubscriptionViewSet, "subscriptions"),
    ("comments", viewsets.CommentViewSet, None),
    ("content-types", viewsets.ContentTypeViewSet, None),
    ("email-addresses", viewsets.EmailAddressViewSet, None),
    ("groups", viewsets.GroupViewSet, None),
    ("log-entries", viewsets.LogEntryViewSet, None),
    ("messages", viewsets.MessageViewSet, None),
    ("permissions", viewsets.PermissionViewSet, None),
    ("posts", viewsets.PostViewSet, None),
    ("users", viewsets.UserViewSet, None),
):
    router.register(prefix, viewset, basename)

urlpatterns = [
    *router.urls,
    path("schema/", SpectacularAPIView.as_view(), name="schema"),
    path(
        "", SpectacularSwaggerView.as_view(url_name="schema"), name="swagger-ui"
    ),
]
