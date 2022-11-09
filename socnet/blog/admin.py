from __future__ import annotations

from django.contrib import admin

from . import models


@admin.register(models.Post)
class PostAdmin(admin.ModelAdmin[models.Post]):
    filter_horizontal = ("likers",)
    list_display = ("id", "user", "date")
    list_filter = ("date", "user")
    search_fields = ("@text",)


@admin.register(models.PostComment)
class PostCommentAdmin(admin.ModelAdmin[models.PostComment]):
    filter_horizontal = ("likers",)
    list_display = ("id", "user", "post", "date")
    list_filter = ("date", "user", "post")
    search_fields = ("@text",)
