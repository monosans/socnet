from __future__ import annotations

from django.urls import path

from . import views

app_name = "users"
urlpatterns = [
    path("account/delete/", views.delete_account_view, name="delete_account"),
    path("profile/edit/", views.edit_profile_view, name="edit_profile"),
    path("users/search/", views.search_users_view, name="search_users"),
]
