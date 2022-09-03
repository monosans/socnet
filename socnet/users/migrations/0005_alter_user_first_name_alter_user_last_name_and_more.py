# Generated by Django 4.1 on 2022-09-03 18:29

from __future__ import annotations

import re

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [("users", "0004_alter_user_username")]

    operations = [
        migrations.AlterField(
            model_name="user",
            name="first_name",
            field=models.CharField(
                blank=True,
                help_text=(
                    "No more than 30 characters. Only English and Russian"
                    " letters and -."
                ),
                max_length=30,
                validators=[
                    django.core.validators.RegexValidator(
                        re.compile("^(?:[\\-A-Za-z]+|[\\-ЁА-яё]+)$")
                    )
                ],
                verbose_name="first name",
            ),
        ),
        migrations.AlterField(
            model_name="user",
            name="last_name",
            field=models.CharField(
                blank=True,
                help_text=(
                    "No more than 30 characters. Only English and Russian"
                    " letters and -."
                ),
                max_length=30,
                validators=[
                    django.core.validators.RegexValidator(
                        re.compile("^(?:[\\-A-Za-z]+|[\\-ЁА-яё]+)$")
                    )
                ],
                verbose_name="last name",
            ),
        ),
        migrations.AlterField(
            model_name="user",
            name="username",
            field=models.CharField(
                db_index=True,
                error_messages={
                    "unique": "A user with that username already exists."
                },
                help_text=(
                    "No more than 30 characters. Only English letters, numbers"
                    " and _. Must begin with a letter and end with a letter or"
                    " number."
                ),
                max_length=30,
                unique=True,
                validators=[
                    django.core.validators.RegexValidator(
                        "^(?:[A-Za-z]|[A-Za-z][\\dA-Z_a-z]*[\\dA-Za-z])$"
                    )
                ],
                verbose_name="username",
            ),
        ),
    ]
