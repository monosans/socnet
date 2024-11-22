from __future__ import annotations

from typing import TYPE_CHECKING

from django.forms import model_to_dict
from django.urls import reverse, reverse_lazy

from socnet.users.forms import EditProfileForm
from socnet.users.models import User
from tests.users.factories import UserFactory
from tests.utils import ClientMethods, auth_client, parametrize_by_get_post

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
    assert response.redirect_chain == [
        ("{}?next={}".format(reverse("account_login"), url), 302)
    ]
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
        url,
        data={
            "username": generated_user.username,
            "display_name": generated_user.display_name,
        },
    )
    assert response.status_code == 200
    new_user = User.objects.only("username", "display_name").get(pk=user.pk)
    assert user.username == new_user.username
    assert user.display_name == new_user.display_name


def test_edit_username_case(client: Client) -> None:
    user = auth_client(client)
    new_username = user.username.swapcase()
    response = client.post(
        url,
        data={"username": new_username, "display_name": user.display_name},
        follow=True,
    )
    assert response.status_code == 200
    new_user = User.objects.only("username").get(pk=user.pk)
    assert response.redirect_chain == [(new_user.get_absolute_url(), 302)]
    assert new_user.username == new_username
