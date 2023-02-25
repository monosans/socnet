from __future__ import annotations

from rest_framework.request import Request

from ..users.models import User


class AuthedRequest(Request):
    user: User
