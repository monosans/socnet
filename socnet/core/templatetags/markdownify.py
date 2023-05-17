from __future__ import annotations

from django import template
from django.utils.safestring import mark_safe

from socnet.core import decorators
from socnet_rs import markdownify

register = template.Library()


register.filter(
    "markdownify", decorators.process_returned_value(mark_safe)(markdownify)
)
