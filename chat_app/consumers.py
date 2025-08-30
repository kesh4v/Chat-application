import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from chat_users.models import User, UserProfile
from django.core.cache import cache
from .models import ChatModel




class PersonalChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):

        sender_id = int(self.scope['url_route']['kwargs']['id'])
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
        # print("Data from client: ", text_data)

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





# ONLINE STATUS OF USERS
class OnlineStatusConsumer(AsyncWebsocketConsumer):
    async def connect(self):

        user = self.scope['user']
        self.group_name = 'user_online_status'

        await self.channel_layer.group_add(
            self.group_name,
            self.channel_name
        )

        await self.accept()

        await self.add_online_user_cache(user.username)
        await self.change_online_status(user, True)

        online_users = await self.get_online_users()

        await self.send(json.dumps({
            'type': 'active_users',
            'users': online_users
        }))

    
    async def disconnect(self, event):
        user = self.scope['user']
        await self.channel_layer.group_discard(
            self.group_name,
            self.channel_name
        )
        await self.remove_online_user_cache(user.username)
        await self.change_online_status(user, False)



    async def change_online_status(self, user, is_online):
        await self.channel_layer.group_send(
            self.group_name,
            {
                'type': 'change_user_status',
                'user': user.username,
                'status': is_online
            }
        )

        await self.update_user_status(user, is_online)

    async def change_user_status(self, event):
        # print("Inside change_user_status", event)
        await self.send(json.dumps({
            'type': 'status_update',
            'user': event['user'],
            'status': event['status']
        }))


    @database_sync_to_async
    def update_user_status(self, user, is_online):
        
        user_profile_obj = UserProfile.objects.get(user__username = user)
        user_profile_obj.online_status = is_online
        user_profile_obj.save()


    @database_sync_to_async
    def add_online_user_cache(self, username):
        cache.add("online_users", set())
        online_users = cache.get("online_users")
        online_users.add(username)
        cache.set("online_users",online_users, None)
        print("After user coming online", cache.get('online_users') or set())
    
    @database_sync_to_async
    def get_online_users(self):
        return list(cache.get("online_users") or set())

    @database_sync_to_async
    def remove_online_user_cache(self, username):
        online_users = cache.get("online_users") or set()
        if username in online_users:
            online_users.remove(username)
            
        cache.set('online_users', online_users, None)
        print("After user going offline", cache.get('online_users') or set())