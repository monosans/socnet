from __future__ import annotations

from django.urls import include, path

from socnet.blog import views

app_name = "blog"

post_patterns = [
    path("", views.posts_view, name="posts"),
    path("<int:pk>/", views.post_view, name="post"),
    path("create/", views.PostCreateView.as_view(), name="post_create"),
    path("<int:pk>/comments/", views.comments_view, name="comments"),
    path("<int:pk>/edit/", views.PostUpdateView.as_view(), name="post_update"),
    path("<int:pk>/delete/", views.post_delete_view, name="post_delete"),
]
comment_patterns = [
    path("edit/", views.CommentUpdateView.as_view(), name="comment_update"),
    path("delete/", views.comment_delete_view, name="comment_delete"),
]
user_patterns = [
    path("", views.user_view, name="user"),
    path("posts/", views.user_posts_view, name="user_posts"),
    path("liked/", views.liked_posts_view, name="liked_posts"),
    path("subscribers/", views.subscribers_view, name="subscribers"),
    path("subscriptions/", views.subscriptions_view, name="subscriptions"),
]
urlpatterns = [
    path("post/", include(post_patterns)),
    path("comment/<int:pk>/", include(comment_patterns)),
    path("@<slug:username>/", include(user_patterns)),
]
