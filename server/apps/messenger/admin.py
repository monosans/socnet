from django.contrib import admin

from . import models


@admin.register(models.Message)
class MessageAdmin(admin.ModelAdmin[models.Message]):
    list_display = ("id", "user", "chat", "date")
    readonly_fields = ("date",)


admin.site.register(models.Chat)
