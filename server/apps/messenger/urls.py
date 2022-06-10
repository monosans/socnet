from django.urls import path

from . import views

urlpatterns = [
    path(
        "<int:pk>/create/", views.chat_get_or_create_view, name="create_chat"
    ),
    path("<int:pk>/", views.chat_detail_view, name="chat"),
    path("", views.chat_list_view, name="chats"),
]
