from __future__ import annotations

from datetime import date
from typing import Optional

from django.contrib.auth.models import AbstractUser
from django.contrib.postgres.fields import CICharField
from django.core.validators import RegexValidator
from django.db import models
from django.urls import reverse
from django.utils.timezone import datetime
from django.utils.translation import gettext_lazy as _

from ..core.fields import (
    LowercaseEmailField,
    NormalizedCharField,
    NormalizedTextField,
)
from . import validators


class User(AbstractUser):
    date_joined = None  # type: ignore[assignment]
    first_name = None  # type: ignore[assignment]
    last_login = None  # type: ignore[assignment]
    last_name = None  # type: ignore[assignment]

    username = CICharField(
        verbose_name=_("username"),
        max_length=32,
        unique=True,
        db_index=True,
        help_text=_(
            "No more than 30 characters. "
            + "Only lowercase English letters, numbers and _. "
            + "Must begin with a letter and end with a letter or number."
        ),
        validators=(RegexValidator(r"^(?:[a-z]|[a-z][\d_a-z]*[\da-z])$"),),
        error_messages={
            "unique": _("A user with that username already exists.")
        },
    )
    display_name = models.CharField(
        verbose_name=_("display name"), max_length=64, blank=True
    )
    email = LowercaseEmailField(verbose_name=_("email address"), unique=True)

    birth_date = models.DateField(
        verbose_name=_("birth date"),
        blank=True,
        null=True,
        validators=(validators.validate_birth_date,),
    )
    location = NormalizedCharField(
        verbose_name=_("location"), max_length=128, blank=True
    )
    image = models.ImageField(
        verbose_name=_("image"), upload_to="user_images/", blank=True
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
        return reverse("blog:user", args=(self.get_username(),))

    def get_full_name(self) -> str:
        return self.display_name

    def get_short_name(self) -> str:
        return self.display_name

    @property
    def display_name_in_parentheses(self) -> str:
        if not self.display_name:
            return ""
        return f"({self.display_name})"

    @property
    def age(self) -> Optional[int]:
        birth_date: Optional[date] = self.birth_date
        if birth_date is None:
            return None
        today = datetime.today()
        # subtract 1 or 0 based on if today precedes the birthdate's month/day
        one_or_zero = (today.month, today.day) < (
            birth_date.month,
            birth_date.day,
        )
        return today.year - birth_date.year - one_or_zero
