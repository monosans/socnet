from django.contrib.auth import get_user_model
from django.http import HttpRequest
from django.shortcuts import get_object_or_404

from ..users.models import User as UserType

User = get_user_model()


def get_user(
    request: HttpRequest, username: str, *prefetch_related: str
) -> UserType:
    if (
        len(prefetch_related) < 2
        and request.user.is_authenticated
        and request.user.get_username() == username
    ):
        return request.user
    qs = (
        User.objects.prefetch_related(*prefetch_related)
        if prefetch_related
        else User
    )
    return get_object_or_404(qs, username=username)  # type: ignore[arg-type]
