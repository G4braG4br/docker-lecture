import json

from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer

from photition_models.models import Notice
from photition_notice.actions import (
    create_notice_action,
    get_initiator_action,
    get_photo_action,
    get_recipient_action,
)


class NoticeConsumer(AsyncWebsocketConsumer):
    data = None

    async def connect(self):
        user = self.scope["user"]

        if user.is_authenticated:
            await self.channel_layer.group_add(f"{user.id}-notices", self.channel_name)
            await self.channel_layer.group_add("global-notices", self.channel_name)
        await self.accept()

    async def receive(self, text_data=None, bytes_data=None):
        self.data = json.loads(text_data)
        print(self.data)
        event = self.get_event()
        initiator = await self.get_initiator()
        photo = await self.get_photo()
        recipient = await self.get_recipient()
        message = self.data.get("message")

        notice = await self.create_notice(event, initiator, photo, recipient, message)

        if recipient is not None:
            await self.channel_layer.group_send(
                f"{recipient.id}-notices",
                {
                    "type": "notice_message",
                    "notice": notice,
                },
            )
        elif message is not None:
            await self.channel_layer.group_send(
                "global-notices", {"type": "notice_message", "notice": notice}
            )

    async def notice_message(self, event):
        await self.send(text_data=json.dumps(event))

    async def disconnect(self, close_code):
        pass

    def get_event(self):
        return self.data.get("event", Notice.Events.GLOBAL)

    @database_sync_to_async
    def get_initiator(self):
        return get_initiator_action(self)

    @database_sync_to_async
    def get_recipient(self):
        return get_recipient_action(self)

    @database_sync_to_async
    def get_photo(self):
        return get_photo_action(self)

    @database_sync_to_async
    def create_notice(
        self,
        event=None,
        initiator=None,
        photo=None,
        recipient=None,
        message=None,
    ):
        return create_notice_action(
            event=event,
            initiator=initiator,
            photo=photo,
            recipient=recipient,
            message=message,
        )
