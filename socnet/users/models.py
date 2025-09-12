from __future__ import annotations

from typing import override
from uuid import uuid4

from django.contrib.auth.models import AbstractUser
from django.core.validators import validate_slug
from django.db import models
from django.urls import reverse
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from socnet.core.fields import (
    NormalizedCharField,
    NormalizedTextField,
    WebpImageField,
)
from socnet.users import validators


def image_upload_to(_instance: User, _filename: str) -> str:
    return f"{uuid4().hex}.webp"


class User(AbstractUser):
    first_name = None  # type: ignore[assignment]
    last_name = None  # type: ignore[assignment]

    username = models.CharField(
        verbose_name=_("username"),
        max_length=32,
        unique=True,
        help_text=_("Only English letters, numbers, underscores and hyphens."),
        validators=(validate_slug,),
        error_messages={
            "unique": _("A user with that username already exists.")
        },
        db_collation="case_insensitive",
    )
    display_name = models.CharField(
        verbose_name=_("display name"), max_length=64
    )
    email = models.EmailField(
        verbose_name=_("email address"),
        unique=True,
        db_collation="case_insensitive",
    )

    show_last_login = models.BooleanField(
        verbose_name=_("show last login time in profile"), default=True
    )
    birth_date = models.DateField(
        verbose_name=_("birth date"),
        blank=True,
        null=True,
        validators=(validators.validate_birth_date,),
    )
    location = NormalizedCharField(
        verbose_name=_("location"), max_length=128, blank=True
    )
    image = WebpImageField(
        verbose_name=_("image"), upload_to=image_upload_to, blank=True
    )
    about = NormalizedTextField(
        verbose_name=_("about me"), max_length=4096, blank=True
    )
    subscriptions = models.ManyToManyField(
        to="self",
        related_name="subscribers",
        symmetrical=False,
        verbose_name=_("subscriptions"),
        blank=True,
    )

    def get_absolute_url(self) -> str:
        return reverse("blog:user", args=(self.username,))

    @override
    def get_full_name(self) -> str:
        return self.display_name

    @override
    def get_short_name(self) -> str:
        return self.display_name

    def get_age(self) -> int | None:
        bd = self.birth_date
        if bd is None:
            return None
        today = timezone.now().date()
        is_bd_later = (today.month, today.day) < (bd.month, bd.day)
        return today.year - bd.year - is_bd_later
