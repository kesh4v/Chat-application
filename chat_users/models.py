from django.db import models
from django.contrib.auth.models import User
from django.templatetags.static import static


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    user_phone_no = models.IntegerField(null=True, blank=True)
    profile_image = models.ImageField(upload_to='profile_img/', null=True, blank=True)
    bio = models.TextField(null=True, blank=True)
    online_status = models.BooleanField(default=False, null=True, blank=True)
    last_seen = models.DateTimeField(auto_now_add=True, null=True, blank=True)

    def __str__(self):
        if self.user.username:
            return self.user.username
        return f"{self.user.first_name} {self.user.last_name}"
    

    def get_profile_image(self):
        if self.profile_image:
            return self.profile_image.url
        return static('images/avatar.svg')
    
    

    
