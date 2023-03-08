# Generated by Django 4.1.7 on 2023-03-08 16:46
from __future__ import annotations

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [("messenger", "0010_alter_chat_members")]

    operations = [
        migrations.AlterField(
            model_name="message",
            name="content",
            field=models.TextField(
                help_text="Supports a safe subset of HTML and Markdown.",
                max_length=4096,
                verbose_name="content",
            ),
        )
    ]
