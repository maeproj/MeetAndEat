# Generated by Django 3.1.4 on 2021-01-10 16:49

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='newuser',
            name='password_date',
            field=models.DateField(default=datetime.date(2021, 1, 10)),
        ),
    ]
