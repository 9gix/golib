from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
    user = models.OneToOneField(User)
    contact = models.CharField(max_length=15)
    address = models.CharField(max_length=250)
    postal = models.CharField(max_length=15, blank=True)
