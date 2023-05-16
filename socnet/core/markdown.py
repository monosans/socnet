from __future__ import annotations

import lxml.etree
import lxml.html
import nh3
from pyromark import Markdown

md = Markdown(extensions=("tables", "strikethrough"))


def markdownify(value: str) -> str:
    html = nh3.clean(md.convert(value))
    try:
        tree = lxml.html.fromstring(html)
    except lxml.etree.LxmlError:
        return html
    for table in tree.xpath("//table"):
        table.set("class", "table")
    for img in tree.xpath("//img"):
        img.set("loading", "lazy")
    return lxml.etree.tostring(tree, encoding=str, method="html")
