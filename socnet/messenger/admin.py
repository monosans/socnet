from __future__ import annotations

from django.contrib import admin

from . import models


@admin.register(models.Message)
class MessageAdmin(admin.ModelAdmin[models.Message]):
    list_display = ("id", "sender", "recipient", "date_created")
    list_filter = ("date_created", "sender", "recipient")
    search_fields = ("@content",)
    readonly_fields = ("date_created",)
