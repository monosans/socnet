from __future__ import annotations

from django.contrib import admin

from . import models


@admin.register(models.Post)
class PostAdmin(admin.ModelAdmin[models.Post]):
    autocomplete_fields = ("likers",)
    list_display = ("id", "user", "date")
    list_filter = ("date",)
    search_fields = ("user__username", "text")


@admin.register(models.PostComment)
class PostCommentAdmin(admin.ModelAdmin[models.PostComment]):
    autocomplete_fields = ("likers",)
    list_display = ("id", "user", "post_id", "date")
    list_filter = ("date",)
    search_fields = ("user__username", "text")
