from django.contrib import admin
from .models import ChatModel
# Register your models here.



@admin.register(ChatModel)
class ChatAdmin(admin.ModelAdmin):
    list_display = ['sender','message','chat_group', 'timestamp']

    