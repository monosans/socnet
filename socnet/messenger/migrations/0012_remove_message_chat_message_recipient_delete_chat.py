# Generated by Django 4.1.7 on 2023-03-08 20:38
from __future__ import annotations

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("messenger", "0011_alter_message_content"),
    ]

    operations = [
        migrations.RemoveField(model_name="message", name="chat"),
        migrations.AddField(
            model_name="message",
            name="recipient",
            field=models.ForeignKey(
                default=1,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="incoming_messages",
                to=settings.AUTH_USER_MODEL,
                verbose_name="recipient",
            ),
            preserve_default=False,
        ),
        migrations.DeleteModel(name="Chat"),
    ]
