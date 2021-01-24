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

class Produkt_rezerwacji(models.Model):
    nazwa_produktu = models.ForeignKey(Menu_item,default=None,on_delete=models.CASCADE,blank=True)
    dodaj_skladnik=models.ManyToManyField(Skladnik,default=None,blank=True,related_name='odejmij_skladnik')
    odejmij_skladnik=models.ManyToManyField(Skladnik,default=None,blank=True,related_name='dodaj_skladnik')
    podanie_godzina = models.IntegerField(default=0,blank=True)
    podanie_minuta = models.IntegerField(default=0,blank=True)
    #def __str__(self):
    #    return self.nazwa_produktu.nazwa
class Reservation(models.Model):
    stolik=models.ManyToManyField(Stolik_item,default=None)
    nazwa = models.ForeignKey(User,default=None,on_delete=models.CASCADE)
    zamowienie_item=models.ManyToManyField(Produkt_rezerwacji,default=None,blank=True)#
    cena_rachunek=models.DecimalField(max_digits=10, decimal_places=2, default=0)
    rezerwacja_dzien = models.CharField(max_length=20)
    time_begin = models.CharField(max_length=10)
    time_end = models.CharField(max_length=10)
    czas_rezerwacji = models.DateTimeField(auto_now_add=True)
    komentarz=models.TextField(blank=True)
    aktywnosc=models.BooleanField(default=True)

class Tymczasowe_zamowienie(models.Model):
    nazwa_uzytkownika = models.ForeignKey(User,default=None,on_delete=models.CASCADE)
    zamowienie_item=models.ManyToManyField(Produkt_rezerwacji,default=None)#
    tymczasowe_edytowane = models.ManyToManyField(Produkt_rezerwacji,default=None,related_name='nazwa_uzytkownika',blank=True)

class Temp_Reservation(models.Model):
    stolik=models.ManyToManyField(Stolik_item,default=None)
    nazwa = models.ForeignKey(User,default=None,on_delete=models.CASCADE)
    rezerwacja_dzien = models.CharField(max_length=20)
    time_begin = models.CharField(max_length=10)
    time_end = models.CharField(max_length=10)
    czas_rezerwacji = models.DateTimeField(auto_now_add=True)





