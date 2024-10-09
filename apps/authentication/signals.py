# TALENTNEXT/apps/authentication/signals.py

from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import User

@receiver(post_save, sender=User)
def reset_first_login(sender, instance, created, **kwargs):
    if created:
        instance.is_first_login = True
        instance.save(update_fields=['is_first_login'])
