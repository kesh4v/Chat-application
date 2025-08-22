from django.db import models
from chat_users.models import User

# Create your models here.

class ChatModel(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    message = models.TextField(null=True, blank=True)
    chat_group = models.CharField(max_length=50, null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.message