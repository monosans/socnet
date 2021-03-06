# Generated by Django 4.0.5 on 2022-06-06 17:35

from django.conf import settings
import django.contrib.auth.models
import django.core.validators
from django.db import migrations, models
import django.utils.timezone
import re
import socnet.users.models
import socnet.users.validators


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('email', models.EmailField(blank=True, max_length=254, verbose_name='email address')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('username', models.CharField(db_index=True, error_messages={'unique': 'A user with that username already exists.'}, help_text='30 characters or less. Lowercase letters, digits and _ only. Must begin with a letter and end with a letter or digit.', max_length=30, unique=True, validators=[django.core.validators.RegexValidator('^(?:[a-z][a-z\\d_]*[a-z\\d]|[a-z])$')], verbose_name='username')),
                ('first_name', models.CharField(blank=True, help_text='30 characters or less. English and Russian letters.', max_length=30, validators=[django.core.validators.RegexValidator(re.compile('^(?:[A-z]+|[??-??]+)$'))], verbose_name='first name')),
                ('last_name', models.CharField(blank=True, help_text='30 characters or less. English and Russian letters.', max_length=30, validators=[django.core.validators.RegexValidator(re.compile('^(?:[A-z]+|[??-??]+)$'))], verbose_name='last name')),
                ('birth_date', models.DateField(blank=True, null=True, validators=[socnet.users.validators.validate_birth_date], verbose_name='birth date')),
                ('location', models.CharField(blank=True, max_length=128, verbose_name='location')),
                ('image', models.ImageField(blank=True, upload_to=socnet.users.models.user_image, verbose_name='image')),
                ('about', models.TextField(blank=True, max_length=1024, verbose_name='about me')),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
                ('subscriptions', models.ManyToManyField(blank=True, related_name='subscribers', to=settings.AUTH_USER_MODEL, verbose_name='subscriptions')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
    ]
