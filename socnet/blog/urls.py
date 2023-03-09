from __future__ import annotations

from django.urls import path

from . import views

app_name = "blog"
urlpatterns = [
    path("posts/", views.posts_view, name="posts"),
    path("post/<int:pk>/", views.post_view, name="post"),
    path("post/create/", views.PostCreateView.as_view(), name="post_create"),
    path("post/<int:pk>/edit/", views.PostUpdateView.as_view(), name="post_update"),
    path("post/<int:pk>/delete/", views.post_delete_view, name="post_delete"),
    path(
        "comment/<int:pk>/edit/",
        views.CommentUpdateView.as_view(),
        name="comment_update",
    ),
    path("comment/<int:pk>/delete/", views.comment_delete_view, name="comment_delete"),
    path("user/<str:username>/", views.user_view, name="user"),
    path("user/<str:username>/posts/", views.user_posts_view, name="user_posts"),
    path("user/<str:username>/liked/", views.liked_posts_view, name="liked_posts"),
    path(
        "user/<str:username>/subscribers/", views.subscribers_view, name="subscribers"
    ),
    path(
        "user/<str:username>/subscriptions/",
        views.subscriptions_view,
        name="subscriptions",
    ),
]
