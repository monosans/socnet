import re
from datetime import date
from typing import Optional

from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
from django.db import models
from django.urls import reverse
from django.utils.timezone import datetime
from django.utils.translation import gettext_lazy as _

from . import validators

EN_RU_REGEX = re.compile(r"^(?:[a-zA-Z\-]+|[а-яА-Я\-]+)$")


def user_image(instance: "User", filename: str) -> str:
    return f"user_{instance.pk}/{filename}"


class User(AbstractUser):
    username = models.CharField(
        verbose_name=_("username"),
        max_length=30,
        unique=True,
        db_index=True,
        help_text=_(
            "No more than 30 characters. "
            + "Only lowercase English letters, numbers and _. "
            + "Must begin with a letter and end with a letter or number."
        ),
        validators=(RegexValidator(r"^(?:[a-z]|[a-z][a-z\d_]*[a-z\d])$"),),
        error_messages={
            "unique": _("A user with that username already exists.")
        },
    )
    first_name = models.CharField(
        verbose_name=_("first name"),
        max_length=30,
        blank=True,
        help_text=_(
            "No more than 30 characters. "
            + "Only English and Russian letters and -."
        ),
        validators=(RegexValidator(EN_RU_REGEX),),
    )
    last_name = models.CharField(
        verbose_name=_("last name"),
        max_length=30,
        blank=True,
        help_text=_(
            "No more than 30 characters. "
            + "Only English and Russian letters and -."
        ),
        validators=(RegexValidator(EN_RU_REGEX),),
    )

    birth_date = models.DateField(
        verbose_name=_("birth date"),
        blank=True,
        null=True,
        validators=(validators.validate_birth_date,),
    )
    location = models.CharField(
        verbose_name=_("location"), max_length=128, blank=True
    )
    image = models.ImageField(
        verbose_name=_("image"), upload_to=user_image, blank=True
    )
    about = models.TextField(
        verbose_name=_("about me"), max_length=4096, blank=True
    )
    subscriptions = models.ManyToManyField(
        to="self",
        related_name="subscribers",
        symmetrical=False,
        verbose_name=_("subscriptions"),
        blank=True,
    )

    class Meta:
        verbose_name = _("user")
        verbose_name_plural = _("users")

    def get_absolute_url(self) -> str:
        return reverse("user", args=(self.get_username(),))

    @property
    def full_name_in_brackets(self) -> str:
        full_name = self.get_full_name()
        if not full_name:
            return ""
        return f"({full_name})"

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
