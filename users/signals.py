from django.db.models.signals import post_save #Import a post_save signal when a user is created
from django.contrib.auth.models import User, Group # Import the built-in User model, which is a sender
from django.dispatch import receiver # Import the receiver
from .models import Profile

@receiver(post_save, sender=User)
def add_to_default_group(sender, instance, created, **kwargs):
    if created:
        default_group = Group.objects.get(name='Colaborador') 
        instance.groups.add(default_group)

@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_profile(sender, instance, **kwargs):
    instance.profile.save()
