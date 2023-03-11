from __future__ import annotations

from django.urls import path
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView
from rest_framework import routers

from . import viewsets

router = routers.SimpleRouter()
for prefix, viewset, basename in (
    ("content_types", viewsets.ContentTypeViewSet, None),
    ("email_addresses", viewsets.EmailAddressViewSet, None),
    ("groups", viewsets.GroupViewSet, None),
    ("log_entries", viewsets.LogEntryViewSet, None),
    ("messages", viewsets.MessageViewSet, None),
    ("permissions", viewsets.PermissionViewSet, None),
    ("comments", viewsets.CommentViewSet, None),
    ("posts", viewsets.PostViewSet, None),
    ("users", viewsets.UserViewSet, None),
    ("comment_like", viewsets.CommentLikeViewSet, "comment_like"),
    ("post_like", viewsets.PostLikeViewSet, "post_like"),
    ("subscription", viewsets.SubscriptionViewSet, "subscription"),
):
    router.register(prefix, viewset, basename)

urlpatterns = [
    *router.urls,
    path("schema/", SpectacularAPIView.as_view(), name="schema"),
    path("", SpectacularSwaggerView.as_view(url_name="schema"), name="swagger-ui"),
]
