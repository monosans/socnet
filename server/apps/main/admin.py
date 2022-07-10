from __future__ import annotations

from django.contrib import admin

from . import models


@admin.register(models.Post)
class PostAdmin(admin.ModelAdmin[models.Post]):
    list_display = ("id", "user", "date")
    filter_horizontal = ("likers",)


@admin.register(models.PostComment)
class PostCommentAdmin(admin.ModelAdmin[models.PostComment]):
    list_display = ("id", "user", "post_id", "date")
    filter_horizontal = ("likers",)
