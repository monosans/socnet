from __future__ import annotations

from django.http import HttpRequest

from .models import User


class AuthedRequest(HttpRequest):
    user: User
