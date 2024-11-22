from __future__ import annotations

from django.urls import path

from socnet.messenger import views

app_name = "messenger"
urlpatterns = [
    path("<slug:username>/", views.chat_view, name="chat"),
    path("", views.chats_view, name="chats"),
]
