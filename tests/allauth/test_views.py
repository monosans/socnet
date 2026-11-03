from __future__ import annotations

import re
from typing import TYPE_CHECKING

from allauth.account.models import EmailAddress
from allauth.account.utils import user_pk_to_url_str
from django.core import mail
from django.urls import reverse, reverse_lazy

from socnet.users.models import User
from tests.users.factories import UserFactory
from tests.utils import auth_client

if TYPE_CHECKING:
    from django.test import Client

PASSWORD = "correct-horse-battery"  # noqa: S105

signup_url = reverse_lazy("account_signup")
login_url = reverse_lazy("account_login")


def get_link(email: mail.EmailMessage) -> str:
    match = re.search(r"https?://[^/\s]+(/\S+)", str(email.body))
    assert match is not None
    return match.group(1)


def create_verified_user() -> User:
    user = UserFactory.create(password=PASSWORD)
    EmailAddress.objects.create(user=user, email=user.email, primary=True, verified=True)
    return user


def test_signup_form(client: Client) -> None:
    response = client.get(signup_url)
    assert response.status_code == 200
    form = response.context["form"]
    assert list(form.fields)[:3] == ["display_name", "email", "username"]
    assert form.fields["email"].widget.attrs["placeholder"] == form.fields["email"].label


def test_signup(client: Client) -> None:
    data = {
        "display_name": "New User",
        "email": "new@example.com",
        "username": "new_user",
        "password1": PASSWORD,
        "password2": PASSWORD,
    }
    response = client.post(signup_url, data=data, follow=True)
    assert response.redirect_chain == [(reverse("account_email_verification_sent"), 302)]
    user = User.objects.get(username="new_user")
    assert user.display_name == "New User"
    assert user.email == "new@example.com"
    assert user.check_password(PASSWORD)
    assert not EmailAddress.objects.get(user=user).verified
    [email] = mail.outbox
    assert email.to == ["new@example.com"]


def test_signup_invalid(client: Client) -> None:
    existing = UserFactory.create()
    data = {
        "display_name": "",
        "email": "new@example.com",
        "username": existing.username,
        "password1": PASSWORD,
        "password2": PASSWORD,
    }
    response = client.post(signup_url, data=data)
    assert response.status_code == 200
    assert set(response.context["form"].errors) == {"display_name", "username"}
    assert User.objects.count() == 1


def test_confirm_email(client: Client) -> None:
    client.post(
        signup_url,
        data={
            "display_name": "New User",
            "email": "new@example.com",
            "username": "new_user",
            "password1": PASSWORD,
            "password2": PASSWORD,
        },
    )
    [email] = mail.outbox
    url = get_link(email)
    response = client.get(url)
    assert response.status_code == 200
    content = response.content.decode()
    assert "new@example.com" in content
    assert "New User (new_user)" in content
    response = client.post(url)
    assert response.status_code == 302
    assert EmailAddress.objects.get(email="new@example.com").verified


def test_confirm_email_invalid_key(client: Client) -> None:
    response = client.get(reverse("account_confirm_email", args=("invalid",)))
    assert response.status_code == 200
    assert "This email confirmation link has expired or is invalid." in response.content.decode()


def test_login_form(client: Client) -> None:
    response = client.get(login_url)
    assert response.status_code == 200
    form = response.context["form"]
    assert form.fields["login"].label == "Username or email"
    assert form.fields["login"].widget.attrs["placeholder"] == "Username or email"
    assert not form.fields["password"].help_text


def test_login_with_username_and_email(client: Client) -> None:
    user = create_verified_user()
    for login in (user.username, user.email.upper()):
        response = client.post(login_url, data={"login": login, "password": PASSWORD})
        assert response.status_code == 302
        assert client.session["_auth_user_id"] == str(user.pk)
        client.logout()


def test_login_unverified_email(client: Client) -> None:
    user = UserFactory.create(password=PASSWORD)
    EmailAddress.objects.create(user=user, email=user.email, primary=True, verified=False)
    response = client.post(
        login_url, data={"login": user.username, "password": PASSWORD}, follow=True
    )
    assert response.redirect_chain == [(reverse("account_email_verification_sent"), 302)]
    assert "_auth_user_id" not in client.session
    [email] = mail.outbox
    assert email.to == [user.email]


def test_logout(client: Client) -> None:
    auth_client(client)
    url = reverse("account_logout")
    response = client.get(url)
    assert response.status_code == 200
    response = client.post(url, follow=True)
    assert response.redirect_chain == [(reverse("account_login"), 302)]
    assert "_auth_user_id" not in client.session


def test_password_reset(client: Client) -> None:
    user = create_verified_user()
    url = reverse("account_reset_password")
    response = client.get(url)
    assert response.status_code == 200
    assert not response.context["form"].fields["email"].label
    response = client.post(url, data={"email": user.email}, follow=True)
    assert response.redirect_chain == [(reverse("account_reset_password_done"), 302)]
    [email] = mail.outbox
    response = client.get(get_link(email), follow=True)
    assert response.status_code == 200
    [(key_url, _)] = response.redirect_chain
    new_password = "another-horse-battery"  # noqa: S105
    response = client.post(
        key_url, data={"password1": new_password, "password2": new_password}, follow=True
    )
    assert response.redirect_chain == [(reverse("account_reset_password_from_key_done"), 302)]
    user.refresh_from_db()
    assert user.check_password(new_password)


def test_password_reset_invalid_key(client: Client) -> None:
    user = create_verified_user()
    url = reverse(
        "account_reset_password_from_key",
        kwargs={"uidb36": user_pk_to_url_str(user), "key": "invalid"},
    )
    response = client.get(url)
    assert response.status_code == 200
    assert response.context["token_fail"]
    response = client.post(url, data={"password1": "x" * 20, "password2": "x" * 20})
    assert response.status_code == 200
    user.refresh_from_db()
    assert user.check_password(PASSWORD)


def test_password_change(client: Client) -> None:
    user = create_verified_user()
    client.force_login(user)
    url = reverse("account_change_password")
    response = client.get(url)
    assert response.status_code == 200
    new_password = "another-horse-battery"  # noqa: S105
    response = client.post(
        url, data={"oldpassword": PASSWORD, "password1": new_password, "password2": new_password}
    )
    assert response.status_code == 302
    user.refresh_from_db()
    assert user.check_password(new_password)


def test_password_set(client: Client) -> None:
    user = auth_client(client)
    user.set_unusable_password()
    user.save()
    client.force_login(user)
    url = reverse("account_set_password")
    response = client.get(url)
    assert response.status_code == 200
    response = client.post(url, data={"password1": PASSWORD, "password2": PASSWORD})
    assert response.status_code == 302
    user.refresh_from_db()
    assert user.check_password(PASSWORD)


def test_email_management(client: Client) -> None:
    user = create_verified_user()
    client.force_login(user)
    url = reverse("account_email")
    response = client.get(url)
    assert response.status_code == 200
    assert user.email in response.content.decode()
    assert not response.context["form"].fields["email"].label
    response = client.post(url, data={"action_add": "", "email": "second@example.com"})
    assert response.status_code == 302
    added = EmailAddress.objects.get(email="second@example.com")
    assert added.user_id == user.pk
    assert not added.verified
    [email] = mail.outbox
    assert email.to == ["second@example.com"]
    response = client.get(url)
    assert response.status_code == 200
    assert "second@example.com" in response.content.decode()


def test_signup_when_logged_in(client: Client) -> None:
    user = auth_client(client)
    response = client.get(signup_url, follow=True)
    assert response.redirect_chain == [(reverse("core:index"), 302), (user.get_absolute_url(), 302)]


def test_signup_keeps_next(client: Client) -> None:
    response = client.get(signup_url, data={"next": "/post/"})
    assert response.status_code == 200
    assert 'value="/post/"' in response.content.decode()


def test_login_inactive_account(client: Client) -> None:
    user = create_verified_user()
    user.is_active = False
    user.save()
    response = client.post(
        login_url, data={"login": user.username, "password": PASSWORD}, follow=True
    )
    assert response.redirect_chain == [(reverse("account_inactive"), 302)]
    assert "This account is inactive." in response.content.decode()
    assert "_auth_user_id" not in client.session


def test_password_reset_when_logged_in(client: Client) -> None:
    user = auth_client(client)
    response = client.get(reverse("account_reset_password"))
    assert response.status_code == 200
    assert "You are already logged in as" in response.content.decode()
    assert f"{user.display_name} ({user.username})" in response.content.decode()


def test_logout_keeps_next(client: Client) -> None:
    auth_client(client)
    url = reverse("account_logout")
    response = client.get(url, data={"next": "/post/"})
    assert response.status_code == 200
    assert 'value="/post/"' in response.content.decode()
    response = client.post(url, data={"next": "/post/"})
    assert response.status_code == 302
    assert response["Location"] == "/post/"
