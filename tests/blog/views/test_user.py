from __future__ import annotations

from typing import TYPE_CHECKING

import pytest
from django.urls import reverse
from django.utils import timezone

from tests.blog.factories import PostFactory
from tests.users.factories import UserFactory
from tests.utils import auth_client, set_image

if TYPE_CHECKING:
    from django.test import Client

    from socnet.users.models import User


def get_url(user: User) -> str:
    return reverse("blog:user", args=(user.username,))


def test_get_self(client: Client) -> None:
    user = auth_client(client)
    response = client.get(get_url(user))
    assert response.status_code == 200


def test_missing_user(client: Client) -> None:
    assert client.get(reverse("blog:user", args=("nobody",))).status_code == 404


def test_counts(client: Client) -> None:
    user = UserFactory.create()
    PostFactory.create_batch(2, author=user)
    PostFactory.create().likers.add(user)
    subscriptions = UserFactory.create_batch(3)
    user.subscriptions.add(*subscriptions)
    subscriptions[0].subscriptions.add(user)
    response = client.get(get_url(user))
    assert response.status_code == 200
    rendered = response.context["user"]
    assert rendered.posts__count == 2
    assert rendered.liked_posts__count == 1
    assert rendered.subscriptions__count == 3
    assert rendered.subscribers__count == 1


@pytest.mark.parametrize("is_subscribed", [True, False])
def test_subscribe_button(client: Client, *, is_subscribed: bool) -> None:
    viewer = auth_client(client)
    user = UserFactory.create()
    if is_subscribed:
        viewer.subscriptions.add(user)
    response = client.get(get_url(user))
    assert response.status_code == 200
    assert response.context["user"].is_subscription == is_subscribed
    content = response.content.decode()
    assert f'data-is-subscribed="{"y" if is_subscribed else "n"}"' in content
    assert reverse("messenger:chat", args=(user.username,)) in content
    assert reverse("users:edit_profile") not in content


def test_own_profile_with_other_case(client: Client) -> None:
    user = auth_client(client, username="Someone")
    response = client.get(reverse("blog:user", args=("sOMEONE",)))
    assert response.status_code == 200
    assert response.context["user"] == user
    content = response.content.decode()
    assert reverse("users:edit_profile") in content
    assert "data-is-subscribed" not in content


@pytest.mark.parametrize("show_last_login", [True, False])
def test_last_login(client: Client, *, show_last_login: bool) -> None:
    now = timezone.now()
    user = UserFactory.create(show_last_login=show_last_login, last_login=now)
    response = client.get(get_url(user))
    assert response.status_code == 200
    last_login_epoch = response.context["user"].last_login_epoch
    if show_last_login:
        assert last_login_epoch == int(now.timestamp())
    else:
        assert last_login_epoch is None
    assert ("Last login" in response.content.decode()) == show_last_login


def test_profile_details(client: Client) -> None:
    today = timezone.now().date()
    user = UserFactory.create(
        birth_date=today.replace(year=today.year - 20), location="Somewhere", about="Line1\nLine2"
    )
    response = client.get(get_url(user))
    assert response.status_code == 200
    content = response.content.decode()
    assert "(20)" in content
    assert "Somewhere" in content
    assert "Line1<br>Line2" in content


def test_image(client: Client) -> None:
    user = UserFactory.create()
    image_src = set_image(user)
    response = client.get(get_url(user))
    assert response.status_code == 200
    assert image_src in response.content.decode()


def test_staff_sees_admin_link(admin_client: Client) -> None:
    user = UserFactory.create()
    response = admin_client.get(get_url(user))
    assert response.status_code == 200
    assert reverse("admin:users_user_change", args=(user.pk,)) in response.content.decode()
