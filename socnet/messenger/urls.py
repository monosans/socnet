from __future__ import annotations

from django.urls import path

from . import views

urlpatterns = [
    path(
        "<int:pk>/get_or_create/",
        views.chat_get_or_create_view,
        name="chat_get_or_create",
    ),
    path("<int:pk>/", views.chat_view, name="chat"),
    path("", views.chats_view, name="chats"),
]
