# Generated by Django 4.1.1 on 2022-09-20 18:22
from __future__ import annotations

from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Post",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "text",
                    models.TextField(
                        blank=True, max_length=4096, verbose_name="text"
                    ),
                ),
                (
                    "image",
                    models.ImageField(
                        blank=True,
                        upload_to="post_images/%Y/%m/%d/",
                        verbose_name="image",
                    ),
                ),
                (
                    "date",
                    models.DateTimeField(
                        auto_now_add=True, verbose_name="date/time"
                    ),
                ),
            ],
            options={"verbose_name": "post", "verbose_name_plural": "posts"},
        ),
        migrations.CreateModel(
            name="PostComment",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "text",
                    models.TextField(
                        blank=True, max_length=4096, verbose_name="text"
                    ),
                ),
                (
                    "image",
                    models.ImageField(
                        blank=True,
                        upload_to="post_comment_images/%Y/%m/%d/",
                        verbose_name="image",
                    ),
                ),
                (
                    "date",
                    models.DateTimeField(
                        auto_now_add=True, verbose_name="date/time"
                    ),
                ),
            ],
            options={
                "verbose_name": "post comment",
                "verbose_name_plural": "post comments",
            },
        ),
    ]
