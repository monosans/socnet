from __future__ import annotations

from django.contrib import admin

from . import models


@admin.register(models.Chat)
class ChatAdmin(admin.ModelAdmin[models.Chat]):
    filter_horizontal = ("participants",)
    list_display = ("id",)
    list_filter = ("participants",)


@admin.register(models.Message)
class MessageAdmin(admin.ModelAdmin[models.Message]):
    list_display = ("id", "user", "chat", "date")
    list_filter = ("date", "user", "chat")
    search_fields = ("text",)
