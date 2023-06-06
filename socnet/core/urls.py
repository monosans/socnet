from __future__ import annotations

from django.urls import path

from . import views

app_name = "core"
urlpatterns = [
    path("manifest.json", views.ManifestView.as_view(), name="manifest"),
    path("", views.index_view, name="index"),
]
