from __future__ import annotations

from django.urls import path

from . import views

app_name = "users"
urlpatterns = [
    path("edit_profile/", views.edit_profile_view, name="edit_profile"),
    path("search_users/", views.search_users_view, name="search_users"),
]
