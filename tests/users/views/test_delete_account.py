from __future__ import annotations

from typing import TYPE_CHECKING

from django.urls import reverse, reverse_lazy

from socnet.users.models import User
from tests.users.factories import UserFactory
from tests.utils import ClientMethods, auth_client, parametrize_by_get_post

if TYPE_CHECKING:
    from django.test import Client

url = reverse_lazy("users:delete_account")


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
    assert User.objects.filter(pk=user.pk).exists()


def test_authed_post_correct_password(client: Client) -> None:
    password = "pw"  # noqa: S105
    user = UserFactory(password=password)
    client.force_login(user)
    response = client.post(url, data={"password": password}, follow=True)
    assert response.redirect_chain == [(reverse("account_login"), 302)]
    assert response.status_code == 200
    assert not User.objects.filter(pk=user.pk).exists()


def test_authed_post_incorrect_password(client: Client) -> None:
    user = auth_client(client, password="pw")  # noqa: S106
    response = client.post(url, data={"password": "pw1"})
    assert response.status_code == 200
    assert User.objects.filter(pk=user.pk).exists()
