import re

from django.utils.translation import gettext_lazy as _

EN_RU_REGEX = re.compile(r"^(?:[A-z]+|[А-я]+)$")
NAME_HELP_TEXT = _("30 characters or less. English and Russian letters.")
