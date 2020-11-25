from django.db import models as mdl
from django.contrib.auth.models import models, User
from django.db.models.signals import post_save
from django.dispatch import receiver
from datetime import date, datetime

class NewUser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    password_date = date(2018, 5, 12)
    let_user_see = 1

@receiver(post_save, sender=User)
def update_profile_signal(sender, instance, created, **kwargs):
    if created:
        NewUser.objects.create(user=instance)
    instance.newuser.save()