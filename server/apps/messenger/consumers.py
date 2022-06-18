import json
from typing import Any, Dict

from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer
from django.urls import reverse

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
        if self.channel_layer is None or self.scope["user"].is_anonymous:
            await self.close()
            return
        self.room_name = self.scope["url_route"]["kwargs"]["chat_pk"]
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
        text_data_json = json.loads(text_data)
        message = text_data_json["message"]
        message_obj = await create_message(
            self.scope["user"], self.room_name, message
        )
        msg = {
            "type": "chat_message",
            "text": message,
            "user__username": message_obj.user.get_username(),
            "user__image": message_obj.user.image.url
            if message_obj.user.image
            else None,
            "date": message_obj.simple_date,
            "user_href": reverse(
                "user", args=(message_obj.user.get_username(),)
            ),
        }
        await self.channel_layer.group_send(self.room_group_name, msg)

    async def chat_message(self, event: Dict[str, Any]) -> None:
        await self.send(text_data=json.dumps(event))
