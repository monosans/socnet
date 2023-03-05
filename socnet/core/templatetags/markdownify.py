from __future__ import annotations

import nh3
from django import template
from django.utils.safestring import SafeString, mark_safe
from django.utils.translation import gettext_lazy as _
from markdown import Markdown

register = template.Library()
md = Markdown(
    extensions=("abbr", "def_list", "fenced_code", "tables", "nl2br", "sane_lists")
)

MARKDOWN_HELP_TEXT = _("Supports a safe subset of HTML and Markdown.")


@register.filter()
def markdownify(value: str) -> SafeString:
    return mark_safe(nh3.clean(md.convert(value)))
