from django.urls import path
from .consumers import PersonalChatConsumer,  OnlineStatusConsumer



websocket_urlpatterns = [
    path('ws/<int:id>/', PersonalChatConsumer.as_asgi()),
    path('ws/status/', OnlineStatusConsumer.as_asgi()),
]