import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from chat_users.models import User
from .models import ChatModel




class PersonalChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        
        sender_id = int(self.scope['url_route']['kwargs']['int'])
        logged_user_id = self.scope['user'].id

        if logged_user_id >= sender_id:
            self.room_name = f'{logged_user_id}-{sender_id}'
        else:
            self.room_name = f'{sender_id}-{logged_user_id}'
        
        self.room_group_name = f'chat_{self.room_name}' 

        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()
        

    async def receive(self, text_data=None, bytes_data=None):
        text_data = json.loads(text_data)
        print("Data from client: ", text_data)

        msg = text_data['message']
        username = text_data['username']
        user_obj = await database_sync_to_async(User.objects.get)(username = username)

        chat_obj = ChatModel(
            sender = user_obj,
            message = msg,
            chat_group = self.room_group_name
        )
        await database_sync_to_async(chat_obj.save)()

        await self.channel_layer.group_send(self.room_group_name, {
                'type': "chat.message",
                'message': text_data
            }
        )

    async def chat_message(self, event):
        await self.send(json.dumps(event['message']))


    async def disconnect(self, code=None, reason=None):
        
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )


        