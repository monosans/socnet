from __future__ import annotations

from django.contrib import admin

from . import models


@admin.register(models.Chat)
class ChatAdmin(admin.ModelAdmin[models.Chat]):
    filter_horizontal = ("members",)
    list_display = ("id",)
    list_filter = ("members",)


@admin.register(models.Message)
class MessageAdmin(admin.ModelAdmin[models.Message]):
    list_display = ("id", "sender", "chat", "date_created")
    list_filter = ("date_created", "sender", "chat")
    search_fields = ("@content",)
    readonly_fields = ("date_created",)
