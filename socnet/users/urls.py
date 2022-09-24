from __future__ import annotations

from django.urls import path

from . import views

app_name = "users"
urlpatterns = [
    path("edit_profile/", views.edit_profile, name="edit_profile"),
    path("search/", views.users_search_view, name="users_search"),
]
