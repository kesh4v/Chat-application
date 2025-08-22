
from django.urls import path
from .views import HomeView, PersonalChatView

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('chat/<str:username>', PersonalChatView.as_view(), name='chat'),
]
