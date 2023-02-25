from __future__ import annotations

from datetime import date, timedelta

from django.core.exceptions import ValidationError
from django.utils import timezone
from django.utils.translation import gettext as _

WORLD_RECORD_FOR_NUMBER_OF_DAYS_LIVED = timedelta(days=44724)


def validate_birth_date(birth_date: date) -> None:
    today = timezone.now().date()
    if birth_date < today - WORLD_RECORD_FOR_NUMBER_OF_DAYS_LIVED:
        raise ValidationError(
            _("You can't be older than the oldest human."), code="unrealistically_old"
        )
    if birth_date > today:
        raise ValidationError(
            _("Are you from the future?"), code="birth_date_in_the_future"
        )
