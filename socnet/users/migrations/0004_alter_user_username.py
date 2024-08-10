# Generated by Django 4.1.3 on 2022-11-06 13:22
from __future__ import annotations

import django.contrib.postgres.fields.citext
import django.core.validators
from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [("users", "0003_alter_user_username")]

    operations = [
        migrations.AlterField(
            model_name="user",
            name="username",
            field=django.contrib.postgres.fields.citext.CICharField(
                db_index=True,
                error_messages={
                    "unique": "A user with that username already exists."
                },
                help_text=(
                    "Only lowercase English letters, numbers and _. Must begin"
                    " with a letter and end with a letter or number."
                ),
                max_length=32,
                unique=False,
                validators=[
                    django.core.validators.RegexValidator(
                        "^(?:[a-z]|[a-z][\\d_a-z]*[\\da-z])$"
                    )
                ],
                verbose_name="username",
            ),
        )
    ]
