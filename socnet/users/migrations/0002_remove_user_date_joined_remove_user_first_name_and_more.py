# Generated by Django 4.1.3 on 2022-11-04 20:11

from __future__ import annotations

import django.contrib.postgres.fields.citext
import django.core.validators
from django.contrib.postgres.operations import CITextExtension
from django.db import migrations, models

import socnet.core.fields


class Migration(migrations.Migration):
    dependencies = [("users", "0001_initial")]

    operations = [
        CITextExtension(),
        migrations.RemoveField(model_name="user", name="date_joined"),
        migrations.RemoveField(model_name="user", name="first_name"),
        migrations.RemoveField(model_name="user", name="last_login"),
        migrations.RemoveField(model_name="user", name="last_name"),
        migrations.AddField(
            model_name="user",
            name="display_name",
            field=models.CharField(
                blank=True, max_length=64, verbose_name="display name"
            ),
        ),
        migrations.AlterField(
            model_name="user",
            name="email",
            field=models.EmailField(
                max_length=254, unique=True, verbose_name="email address"
            ),
        ),
        migrations.AlterField(
            model_name="user",
            name="username",
            field=django.contrib.postgres.fields.citext.CICharField(
                db_index=True,
                error_messages={
                    "unique": "A user with that username already exists."
                },
                help_text=(
                    "No more than 30 characters. Only lowercase English"
                    " letters, numbers and _. Must begin with a letter and end"
                    " with a letter or number."
                ),
                max_length=32,
                unique=True,
                validators=[
                    django.core.validators.RegexValidator(
                        "^(?:[a-z]|[a-z][\\d_a-z]*[\\da-z])$"
                    )
                ],
                verbose_name="username",
            ),
        ),
    ]
