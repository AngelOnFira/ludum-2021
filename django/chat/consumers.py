# chat/consumers.py
import json
from channels.generic.websocket import AsyncWebsocketConsumer, SyncConsumer
from chat.models import Card, Player
from django.db.models import F
from channels.db import database_sync_to_async
from django.db.models import Sum
import asyncio
import logging
import random

log = logging.getLogger(__name__)

from chat.models import COLORS
from chat.serizalizers import CardSerializer


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        log.info("Connect")
        self.group_name = "snek_game"
        self.game = None
        self.username = None
        log.info("User Connected")

        self.player = await self.create_player()

        self.hand = {}
        for i in range(3):
            new_card = await self.create_card()
            self.hand[new_card.id] = new_card
            print(new_card)


        # Join room group
        await self.channel_layer.group_add(self.group_name, self.channel_name)

        await self.accept()

        # await self.send(text_data=json.dumps({"message": total}))
        await self.send_hand()

        # self.my_task = await asyncio.ensure_future(self.run_periodic_task())

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    async def receive(self, bytes_data):
        # print(text_data)
        received = json.loads(bytes_data.decode("utf8"))

        if "card_move" in received:
            id_num = int(received["card_move"]["id"])
            slot = (received["card_move"]["slot"])

            Card.objects.get(id = )

        # await self.send(text_data=json.dumps({"message": total}))

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
        return Player.objects.create()

    @database_sync_to_async
    def add_click(self):
        # self.model = F('click_count') + 1
        self.model.click_count += 1
        self.model.save()

    # @database_sync_to_async
    # def count_total(self):
    #     return ClickTracker.objects.aggregate(Sum("click_count"))

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
            await asyncio.sleep(5550.5)

    @database_sync_to_async
    def create_card(self):
        return Card.objects.create(
            left=random.choice(COLORS)[0],
            right=random.choice(COLORS)[0],
            up=random.choice(COLORS)[0],
            down=random.choice(COLORS)[0],
            main=random.choice(COLORS)[0],
            player=self.player,
        )

    async def send_hand(self):
        serializer = CardSerializer()
        print(repr(serializer))
        await self.send(
            text_data=json.dumps(
                {
                    "message": {
                        "hand": CardSerializer(self.hand.values(), many=True).data
                    }
                }
            )
        )

    def calculate_score(self):
        # player = Player.objects.get(id=self.player)
        self.player.card_set.all()


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