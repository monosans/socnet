from __future__ import annotations

import time
from types import SimpleNamespace
from typing import TYPE_CHECKING

import pytest
from allauth.mfa.models import Authenticator
from allauth.mfa.totp.internal import auth as totp_auth
from django.urls import reverse

from tests.allauth.test_views import PASSWORD, create_verified_user

if TYPE_CHECKING:
    from django.test import Client

    from socnet.users.models import User


@pytest.fixture(autouse=True)
def _freeze_totp_clock(monkeypatch: pytest.MonkeyPatch) -> None:
    # allauth accepts only the current TOTP period, so a code generated near the end of
    # one would be rejected if the period changed before it is checked.
    now = time.time()
    monkeypatch.setattr(totp_auth, "time", SimpleNamespace(time=lambda: now))


def reauthenticate(client: Client, next_url: str) -> None:
    response = client.get(next_url)
    assert response.status_code == 302
    reauthenticate_url = response["Location"]
    assert reauthenticate_url.startswith(reverse("account_reauthenticate"))
    response = client.get(reauthenticate_url)
    assert response.status_code == 200
    response = client.post(reauthenticate_url, data={"password": PASSWORD})
    assert response.status_code == 302
    assert response["Location"] == next_url


def activate_totp(client: Client) -> None:
    url = reverse("mfa_activate_totp")
    reauthenticate(client, url)
    response = client.get(url)
    assert response.status_code == 200
    secret = client.session[totp_auth.SECRET_SESSION_KEY]
    assert secret in response.content.decode()
    [counter] = totp_auth.yield_hotp_counters_from_time()
    code = totp_auth.format_hotp_value(totp_auth.hotp_value(secret, counter))
    response = client.post(url, data={"code": code})
    assert response.status_code == 302


def get_unused_recovery_codes(user: User) -> list[str]:
    authenticator = Authenticator.objects.get(user=user, type=Authenticator.Type.RECOVERY_CODES)
    codes: list[str] = authenticator.wrap().get_unused_codes()
    return codes


def get_recovery_code(user: User) -> str:
    return get_unused_recovery_codes(user)[0]


def test_index_without_mfa(client: Client) -> None:
    client.force_login(create_verified_user())
    response = client.get(reverse("mfa_index"))
    assert response.status_code == 200
    content = response.content.decode()
    assert reverse("mfa_activate_totp") in content
    assert reverse("mfa_deactivate_totp") not in content


def test_activate_totp(client: Client) -> None:
    user = create_verified_user()
    client.force_login(user)
    activate_totp(client)
    assert set(Authenticator.objects.filter(user=user).values_list("type", flat=True)) == {
        Authenticator.Type.TOTP,
        Authenticator.Type.RECOVERY_CODES,
    }
    response = client.get(reverse("mfa_index"))
    assert response.status_code == 200
    content = response.content.decode()
    assert reverse("mfa_deactivate_totp") in content
    assert "10 out of 10 recovery codes are available." in content


def test_activate_totp_wrong_code(client: Client) -> None:
    user = create_verified_user()
    client.force_login(user)
    url = reverse("mfa_activate_totp")
    reauthenticate(client, url)
    response = client.post(url, data={"code": "000000"})
    assert response.status_code == 200
    assert response.context["form"].errors
    assert not Authenticator.objects.filter(user=user).exists()


def test_recovery_codes(client: Client) -> None:
    user = create_verified_user()
    client.force_login(user)
    activate_totp(client)
    response = client.get(reverse("mfa_view_recovery_codes"))
    assert response.status_code == 200
    assert get_recovery_code(user) in response.content.decode()
    old_code = get_recovery_code(user)
    url = reverse("mfa_generate_recovery_codes")
    response = client.get(url)
    assert response.status_code == 200
    response = client.post(url)
    assert response.status_code == 302
    assert get_recovery_code(user) != old_code


def test_login_with_mfa(client: Client) -> None:
    user = create_verified_user()
    client.force_login(user)
    activate_totp(client)
    client.logout()
    response = client.post(
        reverse("account_login"), data={"login": user.username, "password": PASSWORD}
    )
    assert response.status_code == 302
    assert response["Location"] == reverse("mfa_authenticate")
    assert "_auth_user_id" not in client.session
    response = client.get(reverse("mfa_authenticate"))
    assert response.status_code == 200
    code = get_recovery_code(user)
    response = client.post(reverse("mfa_authenticate"), data={"code": code})
    assert response.status_code == 302
    assert client.session["_auth_user_id"] == str(user.pk)
    unused_codes = get_unused_recovery_codes(user)
    assert code not in unused_codes
    assert len(unused_codes) == 9


def test_deactivate_totp(client: Client) -> None:
    user = create_verified_user()
    client.force_login(user)
    activate_totp(client)
    url = reverse("mfa_deactivate_totp")
    response = client.get(url)
    assert response.status_code == 200
    response = client.post(url)
    assert response.status_code == 302
    assert not Authenticator.objects.filter(user=user, type=Authenticator.Type.TOTP).exists()
