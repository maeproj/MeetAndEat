from django.db import models as mdl
from django.contrib.auth.models import models, User
from datetime import date

class NewUser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    password_date = date.today()