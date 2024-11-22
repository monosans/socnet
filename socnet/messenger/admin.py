from __future__ import annotations

from django.contrib import admin

from socnet.messenger import models


@admin.register(models.Message)
class MessageAdmin(admin.ModelAdmin[models.Message]):
    list_display = ("id", "sender", "recipient", "date_created")
    list_filter = ("sender", "recipient", "date_created")
    search_fields = ("@content",)
    readonly_fields = ("date_created",)
