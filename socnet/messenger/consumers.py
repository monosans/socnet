from __future__ import annotations

from typing import Any, Dict, Union

from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncJsonWebsocketConsumer
from channels.layers import InMemoryChannelLayer
from channels_redis.core import RedisChannelLayer
from django.contrib.auth.models import AnonymousUser
from django.db.models import Model

from ..core.templatetags.markdownify import markdownify
from ..users.models import User
from . import models


@database_sync_to_async
def save_obj(obj: Model) -> None:
    obj.full_clean()
    obj.save()


class ChatConsumer(AsyncJsonWebsocketConsumer):
    channel_layer: Union[RedisChannelLayer, InMemoryChannelLayer]

    async def connect(self) -> None:
        user: Union[User, AnonymousUser] = self.scope["user"]
        chat_pk = int(self.scope["url_route"]["kwargs"]["chat_pk"])
        if (
            user.is_anonymous
            or not await database_sync_to_async(
                models.Chat.objects.filter(pk=chat_pk, members=user).exists
            )()
        ):
            await self.close()
            return
        self.room_name = chat_pk
        self.room_group_name = f"chat_{self.room_name}"
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        await self.accept()

    async def disconnect(self, code: int) -> None:  # noqa: ARG002
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    async def receive_json(self, content: Dict[str, str], **kwargs: Any) -> None:
        sender: User = self.scope["user"]
        message = models.Message(
            sender=sender, chat_id=self.room_name, content=content["message"]
        )
        await save_obj(message)
        msg = {
            "type": "chat_message",
            "content": markdownify(message.content),
            "date_created": message.formatted_date_created,
            "sender": {
                "username": sender.get_username(),
                "image": sender.image.url if sender.image else None,
                "href": sender.get_absolute_url(),
            },
        }
        await self.channel_layer.group_send(self.room_group_name, msg)

    async def chat_message(self, event: Dict[str, Any]) -> None:
        await self.send_json(event)
