from __future__ import annotations

from django import template
from django.contrib.admin.templatetags.admin_urls import admin_urlname
from django.db.models import Model
from django.urls import reverse
from django.utils.safestring import SafeString

register = template.Library()


@register.filter()
def obj_admin_url(obj: Model) -> str:
    urlname = admin_urlname(obj._meta, SafeString("change"))  # noqa: SLF001
    return reverse(urlname, args=(obj.pk,))
