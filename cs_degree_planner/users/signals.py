"""
TODO: file description

2023-05-24 - Josh Sawyer : Created a signal dispatcher for "user creation" to link a user to a profile

"""

# https://docs.djangoproject.com/en/4.2/topics/signals/

from django.contrib.auth.models import User
from .models import Profile
from django.db.models.signals import post_save
from django.dispatch import receiver

# When an object is saved, and the sender is from User
@receiver(post_save, sender=User)
def handle_user_created(instance, created, **kwargs): # https://docs.djangoproject.com/en/3.2/ref/signals/#post-save
    if created:
        print("User created, linking user to their profile")
        Profile.objects.create(user=instance)
