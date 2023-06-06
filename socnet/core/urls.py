from __future__ import annotations

from django.urls import path

from . import views

app_name = "core"
urlpatterns = [path("", views.index_view, name="index")]
