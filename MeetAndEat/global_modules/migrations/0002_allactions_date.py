# Generated by Django 3.1.4 on 2021-01-06 18:06

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('global_modules', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='allactions',
            name='date',
            field=models.DateField(default=datetime.datetime(2021, 1, 6, 19, 6, 52, 572708)),
        ),
    ]