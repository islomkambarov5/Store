from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from .models import *


@receiver(pre_save, sender=CustomUser)
def track_is_active_change(sender, instance, **kwargs):
    if instance.pk:
        try:
            previous_instance = sender.objects.get(pk=instance.pk)
            instance._previous_is_active = previous_instance.is_active
        except sender.DoesNotExist:
            instance._previous_is_active = None


@receiver(post_save, sender=CustomUser)
def send_welcome_or_status_update(sender, instance, created, **kwargs):
    if not instance.telegram_id:
        return

    try:
        if created:
            send_message(instance.telegram_id, f"Welcome to our store {instance.username}!")
        else:
            if instance._previous_is_active is False and instance.is_active is True:
                from rest_framework_simplejwt.tokens import RefreshToken
                refresh = RefreshToken.for_user(instance)
                send_message(instance.telegram_id, "Your account has been activated!\n\n"
                                                   f"refresh: {str(refresh)}\n\n"
                                                   f"access: {str(refresh.access_token)}")
            elif instance.is_active is False:
                send_message(instance.telegram_id, "Your account is in a pending state!")
    except Exception as e:
        print(f"Error sending message: {e}")
