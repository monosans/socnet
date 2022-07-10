from __future__ import annotations

from django.contrib import admin

from . import models


@admin.register(models.Chat)
class ChatAdmin(admin.ModelAdmin[models.Chat]):
    list_display = ("id",)
    filter_horizontal = ("participants",)


@admin.register(models.Message)
class MessageAdmin(admin.ModelAdmin[models.Message]):
    list_display = ("id", "user", "chat_id", "date")
