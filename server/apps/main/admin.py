from django.contrib import admin

from . import models


@admin.register(models.Post)
class PostAdmin(admin.ModelAdmin[models.Post]):
    list_display = ("id", "user", "date")
    readonly_fields = ("date",)
    ordering = ("pk",)


@admin.register(models.PostComment)
class PostCommentAdmin(admin.ModelAdmin[models.PostComment]):
    list_display = ("id", "user", "post", "date")
    readonly_fields = ("date",)
