from __future__ import annotations

import lxml.etree
import lxml.html
import nh3
from django import template
from django.utils.safestring import SafeString, mark_safe
from markdown import Markdown

register = template.Library()
md = Markdown(
    extensions=("abbr", "def_list", "fenced_code", "tables", "nl2br", "sane_lists")
)


@register.filter("markdownify")
def markdownify_filter(value: str) -> SafeString:
    return mark_safe(markdownify(value))


def markdownify(value: str) -> str:
    html = nh3.clean(md.convert(value))
    try:
        tree = lxml.html.fromstring(html)
    except lxml.etree.LxmlError:
        return html
    for table in tree.iter("table"):
        table.attrib["class"] = "table"
    for img in tree.iter("img"):
        img.attrib["loading"] = "lazy"
    return lxml.etree.tostring(tree, encoding=str, method="html")
