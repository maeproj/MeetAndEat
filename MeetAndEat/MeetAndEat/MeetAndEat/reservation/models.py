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
    #def __str__(self):
    #    return self.nazwa

class Menu_org(models.Model):
    zawartosc=models.ManyToManyField(Menu_item,default=None)
    #def __str__(self):
    #    return "Menu"

class Reservation(models.Model):
    stolik=models.ManyToManyField(Stolik_item,default=None)
    nazwa = models.ForeignKey(User,default=None,on_delete=models.CASCADE)
    zamowienie_item=models.ManyToManyField(Menu_item,default=None)
    rezerwacja_dzien = models.DateField()
    begin_h = models.IntegerField()
    begin_m = models.IntegerField()
    end_h = models.IntegerField()
    end_m = models.IntegerField()
    czas_rezerwacji = models.DateTimeField(auto_now_add=True)
    komentarz=models.TextField()
    aktywnosc=models.BooleanField(default=True)
    #def __str__(self):
    #    return self.stolik

#    from django.db import models
#from django.contrib.auth.models import User
#from django.core.validators import MaxValueValidator, MinValueValidator

#class Stolik_item(models.Model):
#    stolik_miejsca=models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(16)])
#    #zdjecie=models.ImageField(image="default.png",blank=True)

#class Skladnik(models.Model):
#    nazwa=models.CharField(max_length=20)
#    cena=models.FloatField(validators=[MinValueValidator(0.0), MaxValueValidator(10000.0)])
#    typ=models.CharField(max_length=20)
#    #zdjecie=models.ImageField(image="default.png",blank=True)
#    def __str__(self):
#        return self.nazwa

#class Menu_item(models.Model):
#    typ=models.CharField(max_length=20)
#    nazwa=models.CharField(max_length=50)
#    cena=models.FloatField(validators=[MinValueValidator(0.0), MaxValueValidator(10000.0)])
#    skladniki=models.ManyToManyField(Skladnik,default=None)
#    czas_przygotowania=models.FloatField(default=0.0,validators=[MinValueValidator(0.0), MaxValueValidator(120.0)])
#    #zdjecie=models.ImageField(image="default.png",blank=True)
#    def __str__(self):
#        return self.nazwa

#class Menu_org(models.Model):
#    zawartosc=models.ManyToManyField(Menu_item,default=None)
#    typ=models.CharField(max_length=20)
#    def __str__(self):
#        return self.typ

#class Reservation(models.Model):
#    stolik=models.ManyToManyField(Stolik_item,default=None)
#    nazwa = models.ForeignKey(User,default=None,on_delete=models.CASCADE)
#    cena_rachunek=models.FloatField(validators=[MinValueValidator(0.0), MaxValueValidator(100000.0)])
#    rezerwacja_dzien = models.DateField()
#    begin_h = models.IntegerField()
#    begin_m = models.IntegerField()
#    end_h = models.IntegerField()
#    end_m = models.IntegerField()
#    czas_rezerwacji = models.DateTimeField(auto_now_add=True)
#    komentarz=models.TextField(blank=True)
#    aktywnosc=models.BooleanField(default=True)





