# Generated by Django 4.0.5 on 2022-07-01 13:26

import django.core.validators
from django.db import migrations, models
import re


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_alter_user_first_name_alter_user_last_name_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='about',
            field=models.TextField(blank=True, max_length=4096, verbose_name='about me'),
        ),
        migrations.AlterField(
            model_name='user',
            name='first_name',
            field=models.CharField(blank=True, help_text='No more than 30 characters. Only English and Russian letters and -.', max_length=30, validators=[django.core.validators.RegexValidator(re.compile('^(?:[a-zA-Z\\-]+|[а-яА-Я\\-]+)$'))], verbose_name='first name'),
        ),
        migrations.AlterField(
            model_name='user',
            name='last_name',
            field=models.CharField(blank=True, help_text='No more than 30 characters. Only English and Russian letters and -.', max_length=30, validators=[django.core.validators.RegexValidator(re.compile('^(?:[a-zA-Z\\-]+|[а-яА-Я\\-]+)$'))], verbose_name='last name'),
        ),
        migrations.AlterField(
            model_name='user',
            name='username',
            field=models.CharField(db_index=True, error_messages={'unique': 'A user with that username already exists.'}, help_text='No more than 30 characters. Only lowercase English letters, numbers and _. Must begin with a letter and end with a letter or number.', max_length=30, unique=True, validators=[django.core.validators.RegexValidator('^(?:[a-z]|[a-z][a-z\\d_]*[a-z\\d])$')], verbose_name='username'),
        ),
    ]
