# Generated by Django 4.1.7 on 2023-03-05 14:57
from __future__ import annotations

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("blog", "0006_rename_user_post_author_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="post",
            name="author",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="posts",
                to=settings.AUTH_USER_MODEL,
                verbose_name="author",
            ),
        ),
        migrations.AlterField(
            model_name="postcomment",
            name="author",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="post_comments",
                to=settings.AUTH_USER_MODEL,
                verbose_name="author",
            ),
        ),
    ]
