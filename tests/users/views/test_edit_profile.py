from __future__ import annotations

from typing import TYPE_CHECKING

import pytest
from django.core.files.uploadedfile import SimpleUploadedFile
from django.forms import model_to_dict
from django.urls import reverse, reverse_lazy
from PIL import ExifTags, Image

from socnet.users.forms import EditProfileForm
from socnet.users.models import User
from tests.users.factories import UserFactory
from tests.utils import ClientMethods, auth_client, image_file, parametrize_by_get_post

if TYPE_CHECKING:
    from typing import Any

    from django.test import Client

url = reverse_lazy("users:edit_profile")
fields = EditProfileForm.Meta.fields


def user_to_dict(user: User) -> dict[str, Any]:
    return model_to_dict(user, fields=fields)


@parametrize_by_get_post
def test_unauthed(client: Client, method: ClientMethods) -> None:
    response = (
        client.get(url, follow=True)
        if method == ClientMethods.GET
        else client.post(url, follow=True)
    )
    assert response.redirect_chain == [("{}?next={}".format(reverse("account_login"), url), 302)]
    assert response.status_code == 200


def test_authed_get(client: Client) -> None:
    user = auth_client(client)
    response = client.get(url)
    assert response.status_code == 200
    updated_user = User.objects.only(*fields).get(pk=user.pk)
    assert user_to_dict(user) == user_to_dict(updated_user)


def test_edit_username(client: Client) -> None:
    user = auth_client(client)
    generated_user = UserFactory.build()
    response = client.post(
        url, data={"username": generated_user.username, "display_name": generated_user.display_name}
    )
    assert response.status_code == 200
    new_user = User.objects.only("username", "display_name").get(pk=user.pk)
    assert user.username == new_user.username
    assert user.display_name == new_user.display_name


def test_edit_username_case(client: Client) -> None:
    user = auth_client(client)
    new_username = user.username.swapcase()
    response = client.post(
        url, data={"username": new_username, "display_name": user.display_name}, follow=True
    )
    assert response.status_code == 200
    new_user = User.objects.only("username").get(pk=user.pk)
    assert response.redirect_chain == [(new_user.get_absolute_url(), 302)]
    assert new_user.username == new_username


def test_edit_profile_fields(client: Client) -> None:
    user = auth_client(client, show_last_login=True)
    data = {
        "display_name": "New Name",
        "username": user.username,
        "birth_date": "2000-01-02",
        "location": "  Somewhere  ",
        "about": "About me",
        "show_last_login": False,
    }
    response = client.post(url, data=data, follow=True)
    assert response.redirect_chain == [(user.get_absolute_url(), 302)]
    updated_user = User.objects.only(*fields).get(pk=user.pk)
    assert updated_user.display_name == "New Name"
    assert str(updated_user.birth_date) == "2000-01-02"
    assert updated_user.location == "Somewhere"
    assert updated_user.about == "About me"
    assert not updated_user.show_last_login


@pytest.mark.parametrize(
    ("size", "expected_size"),
    [((2048, 1024), (1024, 512)), ((1024, 2048), (512, 1024)), ((300, 200), (300, 200))],
)
def test_upload_image_is_converted_to_webp(
    client: Client, size: tuple[int, int], expected_size: tuple[int, int]
) -> None:
    user = auth_client(client)
    data = {"display_name": user.display_name, "username": user.username, "image": image_file(size)}
    response = client.post(url, data=data)
    assert response.status_code == 302
    updated_user = User.objects.only("image").get(pk=user.pk)
    assert str(updated_user.image.name).endswith(".webp")
    with updated_user.image.open("rb") as file, Image.open(file) as image:
        assert image.format == "WEBP"
        assert image.size == expected_size


def test_upload_image_applies_exif_orientation(client: Client) -> None:
    user = auth_client(client)
    exif = Image.Exif()
    exif[ExifTags.Base.Orientation] = 6  # Rotated 90 degrees clockwise.
    data = {
        "display_name": user.display_name,
        "username": user.username,
        "image": image_file((200, 100), "JPEG", exif),
    }
    response = client.post(url, data=data)
    assert response.status_code == 302
    updated_user = User.objects.only("image").get(pk=user.pk)
    with updated_user.image.open("rb") as file, Image.open(file) as image:
        assert image.size == (100, 200)


def test_upload_invalid_image(client: Client) -> None:
    user = auth_client(client)
    data = {
        "display_name": user.display_name,
        "username": user.username,
        "image": SimpleUploadedFile("image.png", b"not an image"),
    }
    response = client.post(url, data=data)
    assert response.status_code == 200
    assert "image" in response.context["form"].errors
    assert not User.objects.only("image").get(pk=user.pk).image
