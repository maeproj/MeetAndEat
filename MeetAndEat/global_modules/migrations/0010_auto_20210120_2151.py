# Generated by Django 3.1.4 on 2021-01-20 20:51

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('global_modules', '0009_auto_20210119_2024'),
    ]

    operations = [
        migrations.AlterField(
            model_name='allactions',
            name='date',
            field=models.DateField(default=datetime.datetime(2021, 1, 20, 21, 51, 32, 907873)),
        ),
    ]
