# Generated by Django 3.1.4 on 2021-01-11 18:29

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Menu_item',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('typ', models.CharField(max_length=20)),
                ('nazwa', models.CharField(max_length=50)),
                ('cena', models.DecimalField(decimal_places=2, max_digits=10)),
                ('czas_przygotowania', models.FloatField(default=0.0, validators=[django.core.validators.MinValueValidator(0.0), django.core.validators.MaxValueValidator(120.0)])),
                ('zdjecie', models.ImageField(blank=True, default='default.png', upload_to='gallery')),
            ],
        ),
        migrations.CreateModel(
            name='Skladnik',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nazwa', models.CharField(max_length=20)),
                ('cena', models.DecimalField(decimal_places=2, max_digits=10)),
                ('typ', models.CharField(max_length=20)),
                ('zdjecie', models.ImageField(blank=True, default='default.png', upload_to='gallery')),
            ],
        ),
        migrations.CreateModel(
            name='Stolik_item',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('stolik_miejsca', models.IntegerField(validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(16)])),
                ('zdjecie', models.ImageField(blank=True, default='default.png', upload_to='gallery')),
            ],
        ),
        migrations.CreateModel(
            name='Temp_Reservation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cena_rachunek', models.DecimalField(decimal_places=2, max_digits=10)),
                ('rezerwacja_dzien', models.DateField()),
                ('begin_h', models.IntegerField()),
                ('begin_m', models.IntegerField()),
                ('end_h', models.IntegerField()),
                ('end_m', models.IntegerField()),
                ('czas_rezerwacji', models.DateTimeField(default=None)),
                ('modyfikacje', models.TextField(blank=True)),
                ('komentarz', models.TextField(blank=True)),
                ('aktywnosc', models.BooleanField(default=True)),
                ('nazwa', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('stolik', models.ManyToManyField(default=None, to='reservation.Stolik_item')),
                ('zamowienie_item', models.ManyToManyField(default=None, to='reservation.Menu_item')),
            ],
        ),
        migrations.CreateModel(
            name='Reservation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cena_rachunek', models.DecimalField(decimal_places=2, default=0, max_digits=10)),
                ('rezerwacja_dzien', models.CharField(max_length=20)),
                ('time_begin', models.CharField(max_length=10)),
                ('time_end', models.CharField(max_length=10)),
                ('czas_rezerwacji', models.DateTimeField(auto_now_add=True)),
                ('modyfikacje', models.TextField(blank=True)),
                ('komentarz', models.TextField(blank=True)),
                ('aktywnosc', models.BooleanField(default=True)),
                ('nazwa', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('stolik', models.ManyToManyField(default=None, to='reservation.Stolik_item')),
                ('zamowienie_item', models.ManyToManyField(default=None, to='reservation.Menu_item')),
            ],
        ),
        migrations.CreateModel(
            name='Menu_org',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('typ', models.CharField(max_length=20)),
                ('zawartosc', models.ManyToManyField(default=None, to='reservation.Menu_item')),
            ],
        ),
        migrations.AddField(
            model_name='menu_item',
            name='skladniki',
            field=models.ManyToManyField(blank=True, default=None, to='reservation.Skladnik'),
        ),
    ]
