from django.db import models

class CustomUrl(models.Model):
    token = models.CharField(max_length=100)
