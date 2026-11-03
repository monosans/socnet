from __future__ import annotations

from datetime import timedelta
from typing import TYPE_CHECKING

import pytest
from django.urls import reverse, reverse_lazy
from django.utils import timezone

from socnet.messenger.models import Message
from tests.messenger.factories import MessageFactory
from tests.users.factories import UserFactory
from tests.utils import auth_client, set_image

if TYPE_CHECKING:
    from django.test import Client

    from socnet.users.models import User

chats_url = reverse_lazy("messenger:chats")


def get_chat_url(user: User) -> str:
    return reverse("messenger:chat", args=(user.username,))


def test_chat_unauthed(client: Client) -> None:
    url = get_chat_url(UserFactory.create())
    response = client.get(url, follow=True)
    assert response.redirect_chain == [("{}?next={}".format(reverse("account_login"), url), 302)]
    assert response.status_code == 200


def test_chat_missing_interlocutor(client: Client) -> None:
    auth_client(client)
    response = client.get(reverse("messenger:chat", args=("nobody",)))
    assert response.status_code == 404


# The <template> of each participant renders the message header without pk and epoch.
@pytest.mark.ignore_template_errors
def test_chat_only_shows_own_conversation(client: Client) -> None:
    user = auth_client(client)
    interlocutor = UserFactory.create()
    stranger = UserFactory.create()
    sent = MessageFactory.create(sender=user, recipient=interlocutor, content="sent message")
    received = MessageFactory.create(
        sender=interlocutor, recipient=user, content="received message"
    )
    MessageFactory.create(sender=user, recipient=stranger, content="other chat")
    MessageFactory.create(sender=interlocutor, recipient=stranger, content="private chat")
    response = client.get(get_chat_url(interlocutor))
    assert response.status_code == 200
    assert response.context["interlocutor"] == interlocutor
    assert list(response.context["messages_"]) == [sent, received]
    content = response.content.decode()
    assert "sent message" in content
    assert "received message" in content
    assert "other chat" not in content
    assert "private chat" not in content
    assert f'id="msg{sent.pk}"' in content
    assert f'id="sender-{interlocutor.username.lower()}"' in content


@pytest.mark.ignore_template_errors
def test_chat_with_self(client: Client) -> None:
    user = auth_client(client)
    message = MessageFactory.create(sender=user, recipient=user)
    response = client.get(get_chat_url(user))
    assert response.status_code == 200
    assert list(response.context["messages_"]) == [message]
    content = response.content.decode()
    assert content.count(f'id="sender-{user.username.lower()}"') == 1


def test_chats_unauthed(client: Client) -> None:
    response = client.get(chats_url, follow=True)
    assert response.redirect_chain == [
        ("{}?next={}".format(reverse("account_login"), chats_url), 302)
    ]
    assert response.status_code == 200


def test_chats_empty(client: Client) -> None:
    auth_client(client)
    MessageFactory.create()
    response = client.get(chats_url)
    assert response.status_code == 200
    assert not response.context["chats"]
    assert "You have no chats." in response.content.decode()


def test_chats_lists_interlocutors_by_last_message(client: Client) -> None:
    user = auth_client(client)
    older = UserFactory.create()
    newer = UserFactory.create()
    MessageFactory.create(sender=user, recipient=older, content="first")
    MessageFactory.create(sender=older, recipient=user, content="reply from older")
    MessageFactory.create(sender=newer, recipient=user, content="hello from newer")
    MessageFactory.create(sender=older, recipient=newer)
    response = client.get(chats_url)
    assert response.status_code == 200
    chats = list(response.context["chats"])
    assert chats == [newer, older]
    assert chats[0].last_message_truncated_content == "hello from newer"
    assert chats[1].last_message_truncated_content == "reply from older"
    content = response.content.decode()
    assert get_chat_url(newer) in content
    assert get_chat_url(older) in content


def test_chats_ordered_by_last_message_date(client: Client) -> None:
    user = auth_client(client)
    earlier_pk, later_pk = UserFactory.create_batch(2)
    first = MessageFactory.create(sender=user, recipient=earlier_pk)
    second = MessageFactory.create(sender=later_pk, recipient=user)
    # Give the message created first the later date, so ordering by pk would differ.
    now = timezone.now()
    Message.objects.filter(pk=first.pk).update(date_created=now)
    Message.objects.filter(pk=second.pk).update(date_created=now - timedelta(days=1))
    response = client.get(chats_url)
    assert response.status_code == 200
    assert list(response.context["chats"]) == [earlier_pk, later_pk]


def test_chats_truncates_last_message(client: Client) -> None:
    user = auth_client(client)
    message = MessageFactory.create(sender=user, content="x" * 31)
    response = client.get(chats_url)
    assert response.status_code == 200
    [chat] = response.context["chats"]
    assert chat == message.recipient
    assert chat.last_message_truncated_content == "x" * 30


def test_search_messages(client: Client) -> None:
    user = auth_client(client)
    interlocutor = UserFactory.create()
    sent = MessageFactory.create(sender=user, recipient=interlocutor, content="pineapple pizza")
    received = MessageFactory.create(
        sender=interlocutor, recipient=user, content="I love pineapple"
    )
    MessageFactory.create(sender=user, recipient=interlocutor, content="unrelated")
    MessageFactory.create(content="pineapple of strangers")
    response = client.get(chats_url, data={"q": "pineapple"})
    assert response.status_code == 200
    assert response.context["messages_"] == [(received, interlocutor), (sent, interlocutor)]
    content = response.content.decode()
    assert f"{get_chat_url(interlocutor)}#msg{sent.pk}" in content
    assert f"{get_chat_url(interlocutor)}#msg{received.pk}" in content


def test_search_messages_no_results(client: Client) -> None:
    auth_client(client)
    response = client.get(chats_url, data={"q": "pineapple"})
    assert response.status_code == 200
    assert response.context["messages_"] == []
    assert "No messages found." in response.content.decode()


def test_search_messages_whitespace_query(client: Client) -> None:
    auth_client(client)
    response = client.get(chats_url, data={"q": " "})
    assert response.status_code == 200
    assert response.context["messages_"] is None
    assert response.context["form"].errors == {"q": ["This field is required."]}


@pytest.mark.ignore_template_errors
def test_images(client: Client) -> None:
    user = auth_client(client)
    interlocutor = UserFactory.create()
    user_image_src = set_image(user)
    interlocutor_image_src = set_image(interlocutor)
    MessageFactory.create(sender=user, recipient=interlocutor, content="pineapple")
    MessageFactory.create(sender=interlocutor, recipient=user, content="pineapple")
    chat, chats, search = (
        client.get(get_chat_url(interlocutor)),
        client.get(chats_url),
        client.get(chats_url, data={"q": "pineapple"}),
    )
    for response in (chat, chats, search):
        assert response.status_code == 200
        assert interlocutor_image_src in response.content.decode()
    # Own messages carry the sender's avatar too.
    assert user_image_src in chat.content.decode()
    assert user_image_src in search.content.decode()
