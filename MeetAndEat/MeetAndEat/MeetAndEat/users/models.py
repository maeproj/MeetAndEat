from django.db import models as mdl
from django.contrib.auth.models import models, User
from django.db.models.signals import post_save
from django.dispatch import receiver
from datetime import date, datetime
from django.http import HttpResponse
from phonenumber_field.modelfields import PhoneNumberField

class NewUser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True) #związek z encją User 1:1
    phone = PhoneNumberField(null=False, blank=False, unique=True)
    password_date = models.DateField(default=date(2018, 10, 19)) #data ustanowienia hasła
    entries = models.IntegerField(default=0) #próby logowania
    timeout = models.DateTimeField(null=True) #czasowa blokada w razie przekroczenia maksymalnej liczby prób logowania

    def __str__(self):
        return "{}:{}".format(self.user, self.password_date)