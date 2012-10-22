from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from registration.signals import user_registered

class UserProfile(models.Model):
    user = models.OneToOneField(User)
    contact = models.CharField(max_length=15, blank=True)
    address = models.CharField(max_length=250, blank=True)

def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)

post_save.connect(create_user_profile, sender=User)

def update_user_profile(sender, user, request, **kwargs):
    data = request.POST
    user.first_name = data.get('first_name')
    user.last_name = data.get('last_name')
    user.save()
    user_profile, created = UserProfile.objects.get_or_create(user=user)
    user_profile.address = data.get('address')
    user_profile.contact = data.get('contact')
    user_profile.postal = data.get('postal')
    user_profile.save()

user_registered.connect(update_user_profile)
