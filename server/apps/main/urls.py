from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("edit_profile/", views.edit_profile_view, name="edit_profile"),
    path(
        "post_comment_delete/<int:pk>/",
        views.post_comment_delete_view,
        name="post_comment_delete",
    ),
    path("post/<int:pk>/delete/", views.post_delete_view, name="post_delete"),
    path("post/<int:pk>/", views.post_detail_view, name="post"),
    path("post/", views.post_create_view, name="post_create"),
    path("posts/", views.post_list_view, name="posts"),
    path("search_users/", views.search_users_view, name="search_users"),
    path(
        "user/<str:username>/liked_posts/",
        views.liked_post_list_view,
        name="liked_posts",
    ),
    path(
        "user/<str:username>/subscribers/",
        views.subscriber_list_view,
        name="subscribers",
    ),
    path(
        "user/<str:username>/subscriptions/",
        views.subscription_list_view,
        name="subscriptions",
    ),
    path("user/<str:username>/", views.user_detail_view, name="user"),
]
