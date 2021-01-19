from django.db import models as mdl
from django.contrib.auth.models import models, User
from django.db.models.signals import post_save
from django.dispatch import receiver
from datetime import date, datetime
from django.http import HttpResponse
from phonenumber_field.modelfields import PhoneNumberField

class NewUser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True) #związek z encją User 1:1
    phone = PhoneNumberField(null=False, blank=False, unique=True) #telefon
    password_date = models.DateField(default=date.today()) #data ustanowienia hasła
    entries = models.IntegerField(default=0) #próby logowania
    timeout = models.DateTimeField(null=True) #czasowa blokada w razie przekroczenia maksymalnej liczby prób logowania
    password_history = models.TextField() #historia haseł
    pass_change_entries = models.IntegerField(default=0)
    pass_timeout = models.DateTimeField(null=True, default=None)
    is_worker = models.BooleanField(default=False)

    def __str__(self):
        return "{}:{}".format(self.user, self.password_date)

class SMSModel(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    code = models.CharField(max_length=6, default=False)
    failed_attempts = models.IntegerField(default=0)
    to_delete = models.BooleanField(default=False)