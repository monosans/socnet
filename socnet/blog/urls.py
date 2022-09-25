from __future__ import annotations

from django.urls import path

from . import views

app_name = "blog"
urlpatterns = [
    path("create_post/", views.create_post_view, name="create_post"),
    path(
        "post_comment/<int:pk>/delete/",
        views.post_comment_delete_view,
        name="post_comment_delete",
    ),
    path("post/<int:pk>/delete/", views.post_delete_view, name="post_delete"),
    path("post/<int:pk>/", views.post_view, name="post"),
    path("posts/", views.posts_view, name="posts"),
    path(
        "user/<str:username>/liked_posts/",
        views.liked_posts_view,
        name="liked_posts",
    ),
    path(
        "user/<str:username>/subscribers/",
        views.subscribers_view,
        name="subscribers",
    ),
    path(
        "user/<str:username>/subscriptions/",
        views.subscriptions_view,
        name="subscriptions",
    ),
    path("user/<str:username>/", views.user_view, name="user"),
]
