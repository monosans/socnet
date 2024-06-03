from __future__ import annotations

from typing import TYPE_CHECKING

from django.http import HttpRequest

if TYPE_CHECKING:
    from .models import User


class AuthedRequest(HttpRequest):
    user: User
