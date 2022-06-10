from datetime import date
from typing import Optional

from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
from django.db import models
from django.urls import reverse
from django.utils.timezone import datetime
from django.utils.translation import gettext_lazy as _

from . import constants, validators


def user_image(instance: "User", filename: str) -> str:
    return f"user_{instance.pk}/{filename}"


class User(AbstractUser):
    username = models.CharField(
        verbose_name=_("username"),
        max_length=30,
        unique=True,
        db_index=True,
        help_text=_(
            "30 characters or less. Lowercase letters, digits and _ only."
            + " Must begin with a letter and end with a letter or digit."
        ),
        validators=(RegexValidator(r"^(?:[a-z][a-z\d_]*[a-z\d]|[a-z])$"),),
        error_messages={
            "unique": _("A user with that username already exists.")
        },
    )
    first_name = models.CharField(
        verbose_name=_("first name"),
        max_length=30,
        blank=True,
        help_text=constants.NAME_HELP_TEXT,
        validators=(RegexValidator(constants.EN_RU_REGEX),),
    )
    last_name = models.CharField(
        verbose_name=_("last name"),
        max_length=30,
        blank=True,
        help_text=constants.NAME_HELP_TEXT,
        validators=(RegexValidator(constants.EN_RU_REGEX),),
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
        verbose_name=_("about me"), max_length=1024, blank=True
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

    def __str__(self) -> str:
        return self.username

    def get_absolute_url(self) -> str:
        return reverse("user", args=(self.username,))

    @property
    def full_name_in_brackets(self) -> str:
        if self.first_name and self.last_name:
            return f"({self.first_name} {self.last_name})"
        if self.first_name:
            return f"({self.first_name})"
        if self.last_name:
            return f"({self.last_name})"
        return ""

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
