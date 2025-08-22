from django.shortcuts import render, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View   
from django.contrib.auth.models import User
from .models import ChatModel
from django.contrib.auth import get_user_model, get_user

# from django.contrib


class HomeView(LoginRequiredMixin, View):   # LoginRequiredMixin restrict unauthenticated access 
    def get(self, request):

        users = User.objects.exclude(username = get_user(request))

        # if not request.user.is_authenticated:   # This is other method to redirect unauthenticated user to login
        #     return redirect('signin')  

        return render(request, 'index.html', {'users':users})
    


class PersonalChatView(LoginRequiredMixin, View):
    def get(self, request, username):

        chat_user = User.objects.get(username=username)        
        users = User.objects.exclude(username = get_user(request)) # All active users except the user that is logged in


        # For showing the saved chat messages. Filtering ont the basis of room group name
        current_user = request.user.id
        sender_id = chat_user.id
        # print(sender_id, current_user)
        if current_user >= sender_id:
            room_name = f'{current_user}-{sender_id}'
        else:
            room_name = f'{sender_id}-{current_user}'
        room_group_name = f'chat_{room_name}' 

        chat_obj = ChatModel.objects.filter(chat_group = room_group_name)



        # print("CHAT", chat_obj)

        return render(request, 'chat.html',  {'users':users, 'chat_user':chat_user, 'messages':chat_obj},)