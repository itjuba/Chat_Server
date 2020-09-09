from channels.generic.websocket import AsyncWebsocketConsumer
import json
from accounts.models import Profile
from channels.db import database_sync_to_async
from django.utils import timezone
from django.utils.timezone import localtime, now


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'chat_%s' % self.room_name
        self.user = self.scope["user"]
        print('connect')
        await self.update_user_incr(self.user,1)
        # Join room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        print('disconnect')
        await self.update_user_decr(self.user,0)
        # Leave room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    # Receive message from WebSocket
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']

        # Send message to room group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message,
                'user': str(self.user),
                'time' : str(localtime().now().strftime("%I:%M%p")),
            }
        )

    # Receive message from room group
    async def chat_message(self, event):
        message = event['message']
        username = event['user']
        time = event['time']
        print(self.user.username)

        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'message': message,
            'username' : username,
            'time' : str(time),
        }))

    @database_sync_to_async
    def update_user_incr(self,user,num):
        print('increment')
        print(user.pk)
        return Profile.objects.filter(user=user.pk).update(status=num)


    @database_sync_to_async
    def update_user_decr(self,user,num):
        print('decrement')
        return Profile.objects.filter(user=user.pk).update(status=num)

    @database_sync_to_async
    def nadjib(self):
        print('hello')


