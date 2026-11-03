from __future__ import annotations

from enum import Enum, auto
from io import BytesIO
from typing import TYPE_CHECKING

import pytest
from django.core.files.uploadedfile import SimpleUploadedFile
from PIL import Image

from tests.users.factories import UserFactory

if TYPE_CHECKING:
    from typing import Any

    from django.test import Client

    from socnet.users.models import User


def auth_client(client: Client, **kwargs: Any) -> User:
    user = UserFactory.create(**kwargs)
    client.force_login(user)
    return user


class ClientMethods(Enum):
    GET = auto()
    POST = auto()


parametrize_by_get_post = pytest.mark.parametrize("method", ClientMethods)
parametrize_by_auth = pytest.mark.parametrize("auth", [True, False])
parametrize_by_auth_self = pytest.mark.parametrize(
    ("auth", "self"), [(True, True), (True, False), (False, False)]
)


def image_file(
    size: tuple[int, int], image_format: str = "PNG", exif: Image.Exif | None = None
) -> SimpleUploadedFile:
    with BytesIO() as buffer:
        Image.new("RGB", size, "red").save(buffer, image_format, exif=exif or Image.Exif())
        content = buffer.getvalue()
    return SimpleUploadedFile(f"image.{image_format.lower()}", content)


def set_image(user: User) -> str:
    user.image.save("image.png", image_file((10, 10)))
    return f'src="{user.image.url}"'
