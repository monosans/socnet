from __future__ import annotations

import logging
from typing import TYPE_CHECKING

import orjson
import pytest
from asgiref.sync import async_to_sync
from asgiref.testing import ApplicationCommunicator
from channels.routing import URLRouter
from django.contrib.auth.models import AnonymousUser

from socnet.messenger.models import Message
from socnet.messenger.routing import websocket_urlpatterns
from tests.users.factories import UserFactory

if TYPE_CHECKING:
    from typing import Any

    from socnet.users.models import User

# database_sync_to_async closes the connection when it is not in autocommit mode,
# which breaks the transaction a plain db test runs in.
pytestmark = pytest.mark.django_db(transaction=True)

application = URLRouter(websocket_urlpatterns)


# channels.testing.WebsocketCommunicator can't be imported without daphne, so
# this drives the websocket ASGI events directly.
class Communicator(ApplicationCommunicator):
    def __init__(self, user: User | AnonymousUser, interlocutor_pk: int) -> None:
        scope = {"type": "websocket", "path": f"/ws/chat/{interlocutor_pk}/", "user": user}
        super().__init__(application, scope)

    async def connect(self) -> bool:
        await self.send_input({"type": "websocket.connect"})
        response = await self.receive_output()
        return bool(response["type"] == "websocket.accept")

    async def send_json(self, data: dict[str, Any]) -> None:
        await self.send_input({"type": "websocket.receive", "text": orjson.dumps(data).decode()})

    async def receive_json(self) -> Any:
        response = await self.receive_output()
        assert response["type"] == "websocket.send"
        return orjson.loads(response["text"])

    async def disconnect(self) -> None:
        await self.send_input({"type": "websocket.disconnect", "code": 1000})
        await self.wait()


def test_anonymous_is_rejected() -> None:
    interlocutor = UserFactory.create()

    async def run() -> None:
        communicator = Communicator(AnonymousUser(), interlocutor.pk)
        assert not await communicator.connect()
        await communicator.disconnect()

    async_to_sync(run)()


def test_message_is_saved_and_sent_to_both_participants() -> None:
    sender = UserFactory.create()
    recipient = UserFactory.create()
    outsider = UserFactory.create()

    async def run() -> list[Any]:
        sender_comm = Communicator(sender, recipient.pk)
        recipient_comm = Communicator(recipient, sender.pk)
        outsider_comm = Communicator(outsider, sender.pk)
        communicators = (sender_comm, recipient_comm, outsider_comm)
        for communicator in communicators:
            assert await communicator.connect()
        await sender_comm.send_json({"message": "**hi**"})
        received = [await sender_comm.receive_json(), await recipient_comm.receive_json()]
        assert await outsider_comm.receive_nothing()
        for communicator in communicators:
            await communicator.disconnect()
        return received

    received = async_to_sync(run)()
    message = Message.objects.get()
    assert message.sender_id == sender.pk
    assert message.recipient_id == recipient.pk
    assert message.content == "**hi**"
    expected = {
        "pk": message.pk,
        "content": "<p><strong>hi</strong></p>\n",
        "createdEpoch": int(message.date_created.timestamp()),
        "sender": sender.username,
    }
    assert received == [expected, expected]


def test_invalid_message_is_dropped(caplog: pytest.LogCaptureFixture) -> None:
    sender = UserFactory.create()
    recipient = UserFactory.create()

    async def run() -> None:
        sender_comm = Communicator(sender, recipient.pk)
        recipient_comm = Communicator(recipient, sender.pk)
        for communicator in (sender_comm, recipient_comm):
            assert await communicator.connect()
        await sender_comm.send_json({"message": ""})
        assert await sender_comm.receive_nothing()
        assert await recipient_comm.receive_nothing()
        for communicator in (sender_comm, recipient_comm):
            await communicator.disconnect()

    with caplog.at_level(logging.ERROR, logger="socnet.messenger.consumers"):
        async_to_sync(run)()
    assert not Message.objects.exists()
    [record] = caplog.records
    assert record.exc_info is not None


def test_message_to_missing_user_is_dropped(caplog: pytest.LogCaptureFixture) -> None:
    sender = UserFactory.create()

    async def run() -> None:
        communicator = Communicator(sender, sender.pk + 1)
        assert await communicator.connect()
        await communicator.send_json({"message": "hello"})
        assert await communicator.receive_nothing()
        await communicator.disconnect()

    with caplog.at_level(logging.ERROR, logger="socnet.messenger.consumers"):
        async_to_sync(run)()
    assert not Message.objects.exists()
    assert len(caplog.records) == 1
