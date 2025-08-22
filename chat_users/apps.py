from django.apps import AppConfig


class ChatUsersConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'chat_users'


    def ready(self):
        import chat_users.signals