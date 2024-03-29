from __future__ import annotations

from django import template
from django.contrib.admin.templatetags.admin_urls import admin_urlname
from django.db.models import Model
from django.urls import reverse
from django.utils.safestring import mark_safe

register = template.Library()


@register.filter
def obj_admin_url(obj: Model) -> str:
    urlname = admin_urlname(obj._meta, mark_safe("change"))
    return reverse(urlname, args=(obj.pk,))
