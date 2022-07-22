from __future__ import annotations

from django.contrib import admin

from . import models


@admin.register(models.Chat)
class ChatAdmin(admin.ModelAdmin[models.Chat]):
    filter_horizontal = ("participants",)
    list_display = ("id",)
    search_fields = ("participants__username",)


@admin.register(models.Message)
class MessageAdmin(admin.ModelAdmin[models.Message]):
    list_display = ("id", "user", "chat_id", "date")
    list_filter = ("date",)
    search_fields = ("user__username", "text")
