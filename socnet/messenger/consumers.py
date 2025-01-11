from __future__ import annotations

import logging
from typing import TYPE_CHECKING, override

import orjson
from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncJsonWebsocketConsumer
from django.core.exceptions import ValidationError

from socnet.core.utils import dt_to_epoch
from socnet.messenger import models
from socnet_rs import markdownify

if TYPE_CHECKING:
    from typing import Any, Literal, TypedDict

    from channels.layers import InMemoryChannelLayer
    from channels_redis.core import RedisChannelLayer
    from django.contrib.auth.models import AnonymousUser
    from django.db.models import Model

    from socnet.users.models import User

    class ChatMessageEvent(TypedDict):
        type: Literal["chat_message"]
        pk: int
        content: str
        createdEpoch: int
        sender: str


_logger = logging.getLogger(__name__)


@database_sync_to_async
def save_obj(obj: Model) -> None:
    obj.full_clean()
    obj.save()


class ChatConsumer(AsyncJsonWebsocketConsumer):
    channel_layer: RedisChannelLayer | InMemoryChannelLayer

    @override
    async def connect(self) -> None:
        user: User | AnonymousUser = self.scope["user"]
        if user.is_anonymous:
            await self.close()
            return
        self.interlocutor_pk = int(
            self.scope["url_route"]["kwargs"]["interlocutor_pk"]
        )
        self.group = "chat{}_{}".format(
            *sorted((user.pk, self.interlocutor_pk))
        )
        await self.channel_layer.group_add(self.group, self.channel_name)
        await self.accept()

    @override
    async def disconnect(self, code: int) -> None:
        if not hasattr(self, "group"):
            return
        await self.channel_layer.group_discard(self.group, self.channel_name)

    @override
    async def receive_json(
        self, content: dict[str, str], **kwargs: Any
    ) -> None:
        sender: User = self.scope["user"]
        message = models.Message(
            content=content["message"],
            recipient_id=self.interlocutor_pk,
            sender=sender,
        )
        try:
            await save_obj(message)
        except ValidationError:
            _logger.exception("")
            return
        msg: ChatMessageEvent = {
            "type": "chat_message",
            "pk": message.pk,
            "content": markdownify(message.content),
            "createdEpoch": dt_to_epoch(message.date_created),
            "sender": sender.username,
        }
        await self.channel_layer.group_send(self.group, msg)

    @classmethod
    @override
    async def decode_json(cls, text_data: Any) -> Any:
        return orjson.loads(text_data)

    @classmethod
    @override
    async def encode_json(cls, content: Any) -> str:
        return orjson.dumps(content).decode("utf-8")

    async def chat_message(self, event: ChatMessageEvent) -> None:
        content = {k: v for k, v in event.items() if k != "type"}
        await self.send_json(content)
