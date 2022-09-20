from __future__ import annotations

from django.urls import path

from . import views

urlpatterns = [
    path("", views.index_view, name="index"),
    path("robots.txt", views.RobotsTxtView.as_view()),
]
