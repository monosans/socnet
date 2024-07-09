from __future__ import annotations

from datetime import timedelta
from typing import TYPE_CHECKING

from django.core.exceptions import ValidationError
from django.utils import timezone
from django.utils.translation import gettext as _

if TYPE_CHECKING:
    from datetime import date

WORLD_RECORD_FOR_NUMBER_OF_DAYS_LIVED = timedelta(days=44724)


def validate_birth_date(birth_date: date) -> None:
    today = timezone.now().date()
    if birth_date < today - WORLD_RECORD_FOR_NUMBER_OF_DAYS_LIVED:
        msg = _("Birth date is implausible.")
        code = "unrealistically_old"
        raise ValidationError(msg, code)
    if birth_date > today:
        msg = _("Birth date cannot be in the future.")
        code = "birth_date_in_the_future"
        raise ValidationError(msg, code)
