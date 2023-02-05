from __future__ import annotations

from typing import Any, Dict, Union

from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncJsonWebsocketConsumer
from channels.layers import InMemoryChannelLayer
from channels_redis.core import RedisChannelLayer
from django.contrib.auth.models import AnonymousUser
from django.db.models import Model
from django.utils.html import escape

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
                models.Chat.objects.filter(
                    pk=chat_pk, participants=user
                ).exists
            )()
        ):
            await self.close()
            return
        # pylint: disable-next=attribute-defined-outside-init
        self.room_name = chat_pk
        # pylint: disable-next=attribute-defined-outside-init
        self.room_group_name = f"chat_{self.room_name}"
        await self.channel_layer.group_add(
            self.room_group_name, self.channel_name
        )
        await self.accept()

    async def disconnect(self, code: int) -> None:
        await self.channel_layer.group_discard(
            self.room_group_name, self.channel_name
        )

    async def receive_json(
        self, content: Dict[str, str], **kwargs: Any
    ) -> None:
        user: User = self.scope["user"]
        message = models.Message(
            user=user, chat_id=self.room_name, text=content["message"]
        )
        await save_obj(message)
        msg = {
            "type": "chat_message",
            "text": escape(message.text),
            "date": message.formatted_date,
            "user": {
                "username": user.get_username(),
                "image": user.image.url if user.image else None,
                "href": user.get_absolute_url(),
            },
        }
        await self.channel_layer.group_send(self.room_group_name, msg)

    async def chat_message(self, event: Dict[str, Any]) -> None:
        await self.send_json(event)
