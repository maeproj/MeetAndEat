# Generated by Django 3.1.4 on 2021-01-11 18:29

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('global_modules', '0003_auto_20210110_1749'),
    ]

    operations = [
        migrations.AlterField(
            model_name='allactions',
            name='date',
            field=models.DateField(default=datetime.datetime(2021, 1, 11, 19, 29, 22, 377583)),
        ),
    ]
