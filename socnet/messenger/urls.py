from __future__ import annotations

from django.urls import path

from . import views

app_name = "messenger"
urlpatterns = [
    path("<str:username>/", views.chat_view, name="chat"),
    path("", views.chats_view, name="chats"),
]
