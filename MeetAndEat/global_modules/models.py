from django.db import models
from django.contrib.auth.models import User
from datetime import datetime

class AllActions(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    action_id = models.IntegerField()
    action = models.TextField()
    date = datetime.now()
