# Generated by Django 4.1.7 on 2023-03-05 14:56
from __future__ import annotations

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [("messenger", "0004_alter_message_date_created")]

    operations = [
        migrations.RenameField(
            model_name="message", old_name="user", new_name="sender"
        )
    ]
