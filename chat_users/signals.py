from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth.models import User
from .models import UserProfile



@receiver(post_save, sender=User)
def user_postsave(sender, instance, created, **kwargs):
    user = instance

    if created:
        UserProfile.objects.create(
            user = user,
        )



@receiver(post_save, sender=User)
def send_welcome_mail(sender, instance, created, **kwargs):
    if created:
        send_mail(
            subject = "This is a welcome mail.",
            message = f"Your account is created. Welcome to Keshav's world... {instance.username}",
            from_email = settings.EMAIL_HOST_USER,
            recipient_list = [instance.email],
            fail_silently = False,
        )



