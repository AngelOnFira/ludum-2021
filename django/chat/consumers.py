# chat/consumers.py
import json
from channels.generic.websocket import AsyncWebsocketConsumer, SyncConsumer
from chat.models import ClickTracker
from django.db.models import F
from channels.db import database_sync_to_async
from django.db.models import Sum
import asyncio
import logging

log = logging.getLogger(__name__)


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        log.info("Connect")
        self.group_name = "snek_game"
        self.game = None
        self.username = None
        log.info("User Connected")

        self.model = await self.create_player()

        # Join room group
        await self.channel_layer.group_add(self.group_name, self.channel_name)

        await self.accept()

        total = await self.count_total()

        await self.send(text_data=json.dumps({"message": total}))

        self.my_task = await asyncio.ensure_future(self.run_periodic_task())

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    async def receive(self, bytes_data):
        # print(text_data)
        print(json.loads(bytes_data.decode("utf8")))

        await self.add_click()
        total = await self.count_total()

        await self.send(text_data=json.dumps({"message": total}))

        # text_data_json = json.loads(text_data)
        # message = text_data_json['message']

        # # Send message to room group
        # await self.channel_layer.group_send(
        #     self.room_group_name,
        #     {
        #         'type': 'chat_message',
        #         'message': message
        #     }
        # )

    # Receive message from room group
    async def chat_message(self, event):
        message = event["message"]

        # Send message to WebSocket
        await self.send(text_data=json.dumps({"message": message}))

    @database_sync_to_async
    def create_player(self):
        return ClickTracker.objects.create(click_count=0)

    @database_sync_to_async
    def add_click(self):
        # self.model = F('click_count') + 1
        self.model.click_count += 1
        self.model.save()

    @database_sync_to_async
    def count_total(self):
        return ClickTracker.objects.aggregate(Sum("click_count"))

    async def run_periodic_task(self):
        while True:
            await self.send(
                text_data=json.dumps(
                    {
                        "message": {
                            "hand": [
                                {
                                    "left": "red",
                                    "right": "red",
                                    "up": "red",
                                    "down": "red",
                                    "card": "blue",
                                },
                                {
                                    "left": "green",
                                    "right": "green",
                                    "up": "green",
                                    "down": "red",
                                    "card": "green",
                                },
                            ]
                        }
                    }
                )
            )
            await asyncio.sleep(0.5)


class GameConsumer(SyncConsumer):
    def __init__(self, *args, **kwargs):
        """
        Created on demand when the first player joins.
        """
        super().__init__(*args, **kwargs)
        self.group_name = "snek_game"
        self.engine = GameEngine(self.group_name)
        # Runs the engine in a new thread
        self.engine.start()

    def player_new(self, event):
        self.engine.join_queue(event["player"])

    def player_direction(self, event):
        direction = event.get("direction", "UP")
        self.engine.set_player_direction(event["player"], direction)


# class TimerConsumer(AsyncWebsocketConsumer):
#     async def run_periodic_task(self):
#         while True:
#             await self.send(text_data=json.dumps({"message": 1}))
#             await asyncio.sleep(0.5)

#     async def connect(self):
#         self.my_task = await asyncio.ensure_future(self.run_periodic_task())