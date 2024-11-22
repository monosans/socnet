from __future__ import annotations

from django.urls import path

from socnet.core import views

app_name = "core"
urlpatterns = [
    path("favicon.ico", views.favicon_view, name="favicon"),
    path("manifest.json", views.ManifestView.as_view(), name="manifest"),
    path("", views.index_view, name="index"),
]
