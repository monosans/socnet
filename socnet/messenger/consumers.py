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
        if user.is_anonymous:
            await self.close()
            return
        self.interlocutor_pk = int(self.scope["url_route"]["kwargs"]["interlocutor_pk"])
        self.group = "chat{}_{}".format(*sorted((user.pk, self.interlocutor_pk)))
        await self.channel_layer.group_add(self.group, self.channel_name)
        await self.accept()

    async def disconnect(self, code: int) -> None:  # noqa: ARG002
        await self.channel_layer.group_discard(self.group, self.channel_name)

    async def receive_json(self, content: Dict[str, str], **kwargs: Any) -> None:
        sender: User = self.scope["user"]
        message = models.Message(
            sender=sender, recipient_id=self.interlocutor_pk, content=content["message"]
        )
        await save_obj(message)
        msg = {
            "type": "chat_message",
            "pk": message.pk,
            "content": markdownify(message.content),
            "date_created": message.formatted_date_created,
            "sender": {
                "username": sender.get_username(),
                "display_name": sender.display_name_in_parentheses,
                "image": sender.image.url if sender.image else None,
                "href": sender.get_absolute_url(),
            },
        }
        await self.channel_layer.group_send(self.group, msg)

    async def chat_message(self, event: Dict[str, Any]) -> None:
        await self.send_json(event)
