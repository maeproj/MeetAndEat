# Generated by Django 3.1.4 on 2021-01-22 13:37

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0004_auto_20210120_2151'),
    ]

    operations = [
        migrations.AlterField(
            model_name='newuser',
            name='password_date',
            field=models.DateField(default=datetime.date(2021, 1, 22)),
        ),
    ]
