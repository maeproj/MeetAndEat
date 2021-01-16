from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator

class Stolik_item(models.Model):
    stolik_miejsca=models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(16)])
    zdjecie=models.ImageField(blank=True,upload_to="gallery",default="default.png")

class Skladnik(models.Model):
    nazwa=models.CharField(max_length=20)
    cena=models.DecimalField(max_digits=10, decimal_places=2)
    typ=models.CharField(max_length=20)
    zdjecie=models.ImageField(blank=True,upload_to="gallery",default="default.png")
    def __str__(self):
        return self.nazwa

class Menu_item(models.Model):
    typ=models.CharField(max_length=20)
    nazwa=models.CharField(max_length=50)
    cena=models.DecimalField(max_digits=10, decimal_places=2)
    skladniki=models.ManyToManyField(Skladnik,default=None,blank=True)
    czas_przygotowania=models.FloatField(default=0.0,validators=[MinValueValidator(0.0), MaxValueValidator(120.0)])
    zdjecie=models.ImageField(blank=True,upload_to="gallery",default="default.png")
    def __str__(self):
        return self.nazwa

class Menu_org(models.Model):
    zawartosc=models.ManyToManyField(Menu_item,default=None)
    typ=models.CharField(max_length=20)
    def __str__(self):
        return self.typ

class Reservation(models.Model):
    stolik=models.ManyToManyField(Stolik_item,default=None)
    nazwa = models.ForeignKey(User,default=None,on_delete=models.CASCADE)
    zamowienie_item=models.ManyToManyField(Menu_item,default=None)
    cena_rachunek=models.DecimalField(max_digits=10, decimal_places=2, default=0)
    rezerwacja_dzien = models.CharField(max_length=20)
    time_begin = models.CharField(max_length=10)
    time_end = models.CharField(max_length=10)
    czas_rezerwacji = models.DateTimeField(auto_now_add=True) #ważna zmiana -> usunąłem auto_now_add, trzeba w view dodawać datę
    modyfikacje=models.TextField(blank=True)
    komentarz=models.TextField(blank=True)
    aktywnosc=models.BooleanField(default=True)

class Temp_Reservation(models.Model):
    stolik=models.ManyToManyField(Stolik_item,default=None)
    nazwa = models.ForeignKey(User,default=None,on_delete=models.CASCADE)
    zamowienie_item=models.ManyToManyField(Menu_item,default=None)
    cena_rachunek=models.DecimalField(max_digits=10, decimal_places=2, default=0)
    rezerwacja_dzien = models.CharField(max_length=20)
    time_begin = models.CharField(max_length=10)
    time_end = models.CharField(max_length=10)
    czas_rezerwacji = models.DateTimeField(auto_now_add=True) #ważna zmiana -> usunąłem auto_now_add, trzeba w view dodawać datę
    modyfikacje=models.TextField(blank=True)
    komentarz=models.TextField(blank=True)
    aktywnosc=models.BooleanField(default=True)





