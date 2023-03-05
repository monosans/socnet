from __future__ import annotations

from django.contrib import admin

from . import models


@admin.register(models.Post)
class PostAdmin(admin.ModelAdmin[models.Post]):
    filter_horizontal = ("likers",)
    list_display = ("id", "author", "date_created")
    list_filter = ("date_created", "author")
    search_fields = ("@content",)


@admin.register(models.PostComment)
class PostCommentAdmin(admin.ModelAdmin[models.PostComment]):
    filter_horizontal = ("likers",)
    list_display = ("id", "author", "post", "date_created")
    list_filter = ("date_created", "author", "post")
    search_fields = ("@content",)
