from typing import Any, Dict, Union

from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncJsonWebsocketConsumer
from channels.layers import InMemoryChannelLayer
from django.contrib.auth.models import AbstractBaseUser, AnonymousUser

from ..users.models import User as UserType
from . import models

try:
    from channels_redis.core import RedisChannelLayer
except ImportError:
    pass


class ChatConsumer(AsyncJsonWebsocketConsumer):  # type: ignore[misc]
    channel_layer: Union["RedisChannelLayer", InMemoryChannelLayer]

    async def connect(self) -> None:
        user: Union[AbstractBaseUser, AnonymousUser] = self.scope["user"]
        if user.is_anonymous:
            await self.close()
            return
        self.room_name = int(self.scope["url_route"]["kwargs"]["chat_pk"])
        self.room_group_name = f"chat_{self.room_name}"
        await self.channel_layer.group_add(
            self.room_group_name, self.channel_name
        )
        await self.accept()

    async def disconnect(self, close_code: int) -> None:
        await self.channel_layer.group_discard(
            self.room_group_name, self.channel_name
        )

    async def receive_json(self, content: Dict[str, str]) -> None:
        user: UserType = self.scope["user"]
        message_text = content["message"]
        message_obj: models.Message = await database_sync_to_async(
            models.Message.objects.create
        )(user=user, chat_id=self.room_name, text=message_text)
        msg: Dict[str, str] = {
            "type": "chat_message",
            "text": message_text,
            "user__username": user.get_username(),
            "user__image": user.image.url if user.image else None,
            "date": message_obj.simple_date,
            "user_href": user.get_absolute_url(),
        }
        await self.channel_layer.group_send(self.room_group_name, msg)

    async def chat_message(self, event: Dict[str, Any]) -> None:
        await self.send_json(event)
