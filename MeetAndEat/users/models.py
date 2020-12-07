from django.db import models as mdl
from django.contrib.auth.models import models, User
from django.db.models.signals import post_save
from django.dispatch import receiver
from datetime import date, datetime
from django.http import HttpResponse

class NewUser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    password_date = models.DateField(default=date(2018, 10, 19))
    entries = models.IntegerField(default=0)
    timeout = models.DateTimeField(null=True)

    def __str__(self):
        return "{}:{}".format(self.user, self.password_date)