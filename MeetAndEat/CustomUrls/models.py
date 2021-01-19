from django.db import models
import string
import random

class CustomUrl(models.Model):
    token = models.CharField(max_length=100)
    code = models.CharField(max_length=6, default=''.join(random.choice(string.ascii_letters + string.digits) for i in range(6))