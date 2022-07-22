from __future__ import annotations

from datetime import date

from django.core.exceptions import ValidationError
from django.utils.timezone import datetime, timedelta
from django.utils.translation import gettext as _


def validate_birth_date(birth_date: date) -> None:
    today = datetime.today().date()
    if birth_date < today - timedelta(days=44724):
        raise ValidationError(_("You cannot be older than the oldest human."))
    if birth_date > today:
        raise ValidationError(_("Are you from the future?"))
