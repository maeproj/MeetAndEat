from django.shortcuts import render

#def menu_napoje(request):
#    return render(request, 'menu/menu.html')

#def menu_desery(request):
#    return render(request, 'menu/menu-desery.html')

#def menu_kanapki(request):
#    return render(request, 'menu/menu-kanapki.html')

#def menu_makarony(request):
#    return render(request, 'menu/menu-makarony.html')

#def menu_pizze(request):
#    return render(request, 'menu/menu-pizze.html')

def menu(request):
    return render(request, 'menu/menu.html')

from reservation.models import Skladnik
from reservation.models import Menu_item
from reservation.models import Menu_org

def skladnik_item(request):
    obj=Skladnik.objects.all()
    return render(request,"menu/skladniki.html",{'obj':obj})


def menu_items(request):
    menu_items=Menu_item.objects.all()
    return render(request,"menu/rezerwacje_jedzenie.html",{'menu_items':menu_items})


def menu_orgs(request):
    menu_orgs=Menu_org.objects.all()
    return render(request,"menu\menu.html",{'menu_orgs':menu_orgs})


