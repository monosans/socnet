import json
from typing import Dict

from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer
from django.contrib.auth.models import AbstractBaseUser

from ..users.models import User as UserType
from . import models


async def create_message(
    user: UserType, chat_pk: int, text: str
) -> models.Message:
    message: models.Message = await database_sync_to_async(
        models.Message.objects.create
    )(user=user, chat_id=chat_pk, text=text)
    return message


class ChatConsumer(AsyncWebsocketConsumer):  # type: ignore[misc]
    async def connect(self) -> None:
        user: AbstractBaseUser = self.scope["user"]
        if self.channel_layer is None or user.is_anonymous:
            await self.close()
            return
        self.room_name = int(self.scope["url_route"]["kwargs"]["chat_pk"])
        self.room_group_name = f"chat_{self.room_name}"
        await self.channel_layer.group_add(
            self.room_group_name, self.channel_name
        )
        await self.accept()

    async def disconnect(self, close_code: int) -> None:
        if self.channel_layer is None:
            return
        await self.channel_layer.group_discard(
            self.room_group_name, self.channel_name
        )

    async def receive(self, text_data: str) -> None:
        if self.channel_layer is None:
            return
        user: UserType = self.scope["user"]
        text_data_json: Dict[str, str] = json.loads(text_data)
        message = text_data_json["message"]
        message_obj = await create_message(user, self.room_name, message)
        msg: Dict[str, str] = {
            "type": "chat_message",
            "text": message,
            "user__username": user.get_username(),
            "user__image": user.image.url if user.image else None,
            "date": message_obj.simple_date,
            "user_href": user.get_absolute_url(),
        }
        await self.channel_layer.group_send(self.room_group_name, msg)

    async def chat_message(self, event: Dict[str, str]) -> None:
        await self.send(text_data=json.dumps(event))
