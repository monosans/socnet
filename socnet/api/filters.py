from __future__ import annotations

from allauth.account.models import EmailAddress
from django.contrib.admin.models import LogEntry
from django.contrib.auth import models as auth_models
from django.contrib.contenttypes.models import ContentType
from django_filters import FilterSet

from ..blog import models as blog_models
from ..messenger import models as messenger_models
from ..users.models import User

ID_FIELDS = ["exact", "in"]
BOOL_FIELDS = ["exact"]
LOWERCASE_CHAR_FIELDS = ["exact", "contains", "in", "startswith", "endswith"]
CHAR_FIELDS = [
    *LOWERCASE_CHAR_FIELDS,
    "iexact",
    "icontains",
    "istartswith",
    "iendswith",
]
DATE_FIELDS = [
    "exact",
    "in",
    "gt",
    "gte",
    "lt",
    "lte",
    "range",
    "year",
    "iso_year",
    "month",
    "day",
    "week",
    "week_day",
    "iso_week_day",
    "quarter",
]
DATETIME_FIELDS = [*DATE_FIELDS, "date", "time", "hour", "minute", "second"]
NULLABLE = ["isnull"]

BASE_FIELDS = {"id": ID_FIELDS}


class ChatFilter(FilterSet):
    class Meta:
        model = messenger_models.Chat
        fields = BASE_FIELDS.copy()


class ContentTypeFilter(FilterSet):
    class Meta:
        model = ContentType
        fields = dict(
            BASE_FIELDS, app_label=LOWERCASE_CHAR_FIELDS, model=LOWERCASE_CHAR_FIELDS
        )


class EmailAddressFilter(FilterSet):
    class Meta:
        model = EmailAddress
        fields = dict(
            BASE_FIELDS,
            email=LOWERCASE_CHAR_FIELDS,
            verified=BOOL_FIELDS,
            primary=BOOL_FIELDS,
            user=ID_FIELDS,
        )


class GroupFilter(FilterSet):
    class Meta:
        model = auth_models.Group
        fields = dict(BASE_FIELDS, name=CHAR_FIELDS)


class LogEntryFilter(FilterSet):
    class Meta:
        model = LogEntry
        fields = dict(
            BASE_FIELDS,
            action_time=DATETIME_FIELDS,
            object_id=[*ID_FIELDS, *NULLABLE],
            object_repr=CHAR_FIELDS,
            action_flag=ID_FIELDS,
            change_message=CHAR_FIELDS,
            user=ID_FIELDS,
            content_type=[*ID_FIELDS, *NULLABLE],
        )


class MessageFilter(FilterSet):
    class Meta:
        model = messenger_models.Message
        fields = dict(
            BASE_FIELDS,
            content=CHAR_FIELDS,
            date_created=DATETIME_FIELDS,
            sender=ID_FIELDS,
            chat=ID_FIELDS,
        )


class PermissionFilter(FilterSet):
    class Meta:
        model = auth_models.Permission
        fields = dict(
            BASE_FIELDS,
            name=CHAR_FIELDS,
            codename=LOWERCASE_CHAR_FIELDS,
            content_type=ID_FIELDS,
        )


class PostCommentFilter(FilterSet):
    class Meta:
        model = blog_models.PostComment
        fields = dict(
            BASE_FIELDS,
            content=CHAR_FIELDS,
            date_created=DATETIME_FIELDS,
            date_updated=DATETIME_FIELDS,
            post=ID_FIELDS,
            author=ID_FIELDS,
        )


class PostFilter(FilterSet):
    class Meta:
        model = blog_models.Post
        fields = dict(
            BASE_FIELDS,
            content=CHAR_FIELDS,
            date_created=DATETIME_FIELDS,
            date_updated=DATETIME_FIELDS,
            author=ID_FIELDS,
        )


class UserFilter(FilterSet):
    class Meta:
        model = User
        fields = dict(
            BASE_FIELDS,
            is_superuser=BOOL_FIELDS,
            is_staff=BOOL_FIELDS,
            is_active=BOOL_FIELDS,
            username=LOWERCASE_CHAR_FIELDS,
            display_name=CHAR_FIELDS,
            email=LOWERCASE_CHAR_FIELDS,
            birth_date=[*DATE_FIELDS, *NULLABLE],
            location=CHAR_FIELDS,
            about=CHAR_FIELDS,
        )
