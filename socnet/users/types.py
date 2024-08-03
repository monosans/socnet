# ruff: noqa: A005
from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from django.http import HttpRequest

    from .models import User

    class AuthedRequest(HttpRequest):
        user: User
