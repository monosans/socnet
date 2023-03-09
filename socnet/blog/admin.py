from __future__ import annotations

from django.contrib import admin

from . import models


@admin.register(models.Post)
class PostAdmin(admin.ModelAdmin[models.Post]):
    filter_horizontal = ("likers",)
    list_display = ("id", "author", "date_created", "date_updated")
    list_filter = ("date_created", "date_updated", "author")
    search_fields = ("@content",)
    readonly_fields = ("date_created", "date_updated")


@admin.register(models.Comment)
class CommentAdmin(admin.ModelAdmin[models.Comment]):
    filter_horizontal = ("likers",)
    list_display = ("id", "author", "post", "date_created", "date_updated")
    list_filter = ("date_created", "date_updated", "author", "post")
    search_fields = ("@content",)
    readonly_fields = ("date_created", "date_updated")
