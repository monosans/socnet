from __future__ import annotations

import lxml.etree
import lxml.html
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


def bootstrapify(tree: lxml.etree._Element) -> None:  # noqa: SLF001
    for table in tree.iter("table"):
        table.attrib["class"] = "table"


def lazy_img(tree: lxml.etree._Element) -> None:  # noqa: SLF001
    for img in tree.iter("img"):
        img.attrib["loading"] = "lazy"


@register.filter()
def markdownify(value: str) -> SafeString:
    sanitized_html = nh3.clean(md.convert(value))
    tree = lxml.html.fromstring(sanitized_html)
    bootstrapify(tree)
    lazy_img(tree)
    tree_str = lxml.etree.tostring(tree, encoding=str, method="html")
    return mark_safe(tree_str)
