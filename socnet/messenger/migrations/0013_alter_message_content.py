# Generated by Django 4.2.1 on 2023-05-28 15:32
from __future__ import annotations

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("messenger", "0012_remove_message_chat_message_recipient_delete_chat")
    ]

    operations = [
        migrations.AlterField(
            model_name="message",
            name="content",
            field=models.TextField(
                help_text="Supports a safe subset of HTML and Markdown.",
                max_length=16384,
                verbose_name="content",
            ),
        )
    ]
