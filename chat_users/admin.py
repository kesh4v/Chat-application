from django.contrib import admin
from .models import UserProfile


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['user','first_name','bio', 'user_phone_no', 'online_status']

    def first_name(self, obj):
        return obj.user.first_name


