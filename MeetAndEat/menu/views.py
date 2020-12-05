from django.shortcuts import render

def menu_napoje(request):
    return render(request, 'menu/menu.html')

def menu_desery(request):
    return render(request, 'menu/menu-desery.html')

def menu_kanapki(request):
    return render(request, 'menu/menu-kanapki.html')

def menu_makarony(request):
    return render(request, 'menu/menu-makarony.html')

def menu_pizze(request):
    return render(request, 'menu/menu-pizze.html')


