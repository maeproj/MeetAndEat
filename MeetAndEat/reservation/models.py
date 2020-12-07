from django.db import models
from django.contrib.auth.models import User


class Stolik_item(models.Model):
    stolik_miejsca=models.IntegerField()
    #zdjecie=models.ImageField(image="default.png",blank=True)


class Skladnik(models.Model):
    nazwa=models.CharField(max_length=20)
    cena=models.FloatField()
    typ=models.CharField(max_length=20)
    #zdjecie=models.ImageField(image="default.png",blank=True)

class Menu_item(models.Model):
    typ=models.CharField(max_length=20)
    nazwa=models.CharField(max_length=50)
    cena=models.FloatField()
    skladniki=models.ManyToManyField(Skladnik,default=None)
    czas_przygotowania=models.FloatField()
    #zdjecie=models.ImageField(image="default.png",blank=True)
    def __str__(self):
        return self.nazwa

class Menu_org(models.Model):
    zawartosc=models.ManyToManyField(Menu_item,default=None)
    def __str__(self):
        return "Menu"

class Reservation(models.Model):
    stolik=models.ManyToManyField(Stolik_item,default=None)
    nazwa = models.ForeignKey(User,default=None,on_delete=models.CASCADE)
    zamowienie_item=models.ManyToManyField(Menu_item,default=None)
    rezerwacja_dzien = models.DateField()
    begin_h = models.CharField(max_length=10)
    begin_m = models.CharField(max_length=10)
    end_h = models.CharField(max_length=10)
    end_m = models.CharField(max_length=10)
    czas_rezerwacji = models.DateTimeField(auto_now_add=True)
    komentarz=models.TextField()
    aktywnosc=models.BooleanField(default=True)
    def __str__(self):
        return self.stolik






