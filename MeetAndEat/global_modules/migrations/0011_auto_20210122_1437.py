# Generated by Django 3.1.4 on 2021-01-22 13:37

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('global_modules', '0010_auto_20210120_2151'),
    ]

    operations = [
        migrations.AlterField(
            model_name='allactions',
            name='date',
            field=models.DateField(default=datetime.datetime(2021, 1, 22, 14, 37, 1, 21387)),
        ),
    ]
