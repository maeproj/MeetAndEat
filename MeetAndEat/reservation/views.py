from decimal import Decimal
from django.shortcuts import render, redirect
from django.http import HttpResponse
from .forms import ReservationForm, PickForm,dodaj_dania_do_rezerwacji,zamowienie_tymczasowe,dodaj_edytowane_danie
from users.forms import UserLoginForm
from django.contrib.auth.decorators import login_required
from datetime import date, time, datetime, timedelta
from django.contrib import messages
from .models import Temp_Reservation, Stolik_item, Reservation,Stolik_item, Tymczasowe_zamowienie,Produkt_rezerwacji,Menu_item, Skladnik
from copy import deepcopy
import numpy as np
import pdb
from global_modules.models import AllActions

class Helper_class:
    def __init__(self, stolik, nazwa, rezerwacja_dzien, time_begin, time_end):
        self.stolik = stolik
        self.nazwa = nazwa
        self.rezerwacja_dzen = rezerwacja_dzien
        self.time_begin = time_begin
        self.time_end = time_end

class AvailableDate: 
    def __init__(self, begin_time, end_time, day, reservations, stolik):
        self.times = [[16, 0],
                      [16, 15],
                      [16, 30],
                      [16, 45],
                      [17, 0],
                      [17, 15],
                      [17, 30],
                      [17, 45],
                      [18, 0],
                      [18, 15],
                      [18, 30],
                      [18, 45],
                      [19, 0],
                      [19, 15],
                      [19, 30],
                      [19, 45],
                      [20, 0],
                      [20, 15],
                      [20, 30],
                      [20, 45],
                      [21, 0],
                      [21, 15],
                      [21, 30],
                      [21, 45]]
        self.times_table = [deepcopy(self.times), deepcopy(self.times), deepcopy(self.times), deepcopy(self.times), deepcopy(self.times)]
        self.time_in_minutes = (end_time[0]*60 + end_time[1]) - (begin_time[0]*60 + begin_time[1])
        self.res = reservations
        self.day = day
        self.begin_time = begin_time
        self.end_time = end_time
        self.stolik = stolik
        self.alternatives = [(0, 0, 0, 0), (0, 0, 0, 0), (0, 0, 0, 0), (0, 0, 0, 0), (0, 0, 0, 0)]
        self.save_begin = None
        self.save_end = None
        for d in self.res:
            self.save_begin, self.save_end = None, None
            s1, s2, s3, s4 = 2, 2, 2, 2
            l1 = d.time_begin.find(':')
            l2 = d.time_end.find(':')
            le1 = len(d.time_begin)
            le2 = len(d.time_end)
            if l1 < 2:
                s1 = 1
            if le1 + (2 - s1) < 5:
                s2 = 1
            if l2 < 2:
                s3 = 1
            if le2 + (2 - s3) < 5:
                s4 = 1
            for i, time in enumerate(self.times):
                if time[0] == int(d.time_begin[0:s1]) and time[1] == int(d.time_begin[-s2:]):
                    self.save_begin = i
                elif time[0] == int(d.time_end[0:s3]) and time[1] == int(d.time_end[-s4:]):
                    self.save_end = i + 1

            if self.save_begin is not None and self.save_end is not None:
                del self.times[self.save_begin:self.save_end]

    def return_accept(self):
#Stolik pożądany
        check_begin, check_end, search_further = False, False, True
        if self.begin_time in self.times and self.end_time in self.times:
            return 'reserve'
        start, success = True, False
        new_time = None
        if self.begin_time in self.times:
            new_time = [self.end_time[0], self.end_time[1] - 15]
            if new_time[1] < 0:
                new_time[0] -= 1
                new_time[1] = 45
            while(start):
                if new_time[0] < self.begin_time[0] or new_time[0] == self.begin_time[0] and new_time[1] <= self.begin_time[1]:
                    start = False
                    break
                if new_time in self.times:
                    start = False
                    success = True
                    break
                new_time = [new_time[0], new_time[1] - 15]
                if new_time[1] < 0:
                    new_time[0] -= 1
                    new_time[1] = 45

            if success:
                h = (new_time[0]*60 + new_time[1]) - (self.begin_time[0] * 60 + self.begin_time[1])
                if h >= 45:
                    self.alternatives[self.stolik.stolik_miejsca - 1] = [self.stolik.stolik_miejsca, f'Możliwa rezerwacja na wybrany termin na {h} minut zamiast na {self.time_in_minutes} minut',\
                       f'{self.begin_time[0]}' + ':' + f'{self.begin_time[1]}', f'{new_time[0]}' + ':' + f'{new_time[1]}']
                    search_further = False
                

        if search_further:
            start = True
            new_time = [self.begin_time[0], self.begin_time[1] + 15]
            if new_time[1] > 45:
                new_time[0] += 1
                new_time[1] = 0
            while(start):
                if new_time[0] > 21:
                    start = False
                    self.alternatives[self.stolik.stolik_miejsca - 1] = [self.stolik.stolik_miejsca, f'Brak możliwości na dany dzień', '0', '0']
                    break
                if new_time in self.times:
                    new_end_time = [new_time[0], new_time[1] + 30]
                    if new_end_time[1] > 45:
                        new_end_time[0] += 1
                        new_end_time[1] = np.mod(new_time[1] + 30, 60)
                    nonstop, success = True, True
                    while(nonstop):
                        if new_end_time in self.times:
                            if (new_end_time[0]*60 + new_end_time[1]) - (new_time[0]*60 + new_time[1]) == self.time_in_minutes:
                                nonstop = False
                                break
                            new_end_time = [new_end_time[0], new_end_time[1] + 15]
                            if new_end_time[1] > 45:
                                new_end_time[0] += 1
                                new_end_time[1] = 0
                            continue

                        if new_end_time[0]*60 + new_end_time[1] == new_time[0]*60 + new_time[1] + 30:
                            success = False

                        nonstop = False
                        break

                    if success:
                        time = (new_end_time[0]*60 + new_end_time[1]) - (new_time[0]*60 + new_time[1])
                        if time == self.time_in_minutes:
                            self.alternatives[self.stolik.stolik_miejsca - 1] = [self.stolik.stolik_miejsca, f'Możliwa rezerwacja na godzine {new_time[0]}:{new_time[1]} na {time} minut',\
                               f'{new_time[0]}' + ':' + f'{new_time[1]}', f'{new_end_time[0]}' + ':' + f'{new_end_time[1]}']
                        else:
                            self.alternatives[self.stolik.stolik_miejsca - 1] = [self.stolik.stolik_miejsca, f'Możliwa rezerwacja na godzine {new_time[0]}:{new_time[1]} na {time} minut\n zamiast na {self.time_in_minutes} minut',\
                               f'{new_time[0]}' + ':' + f'{new_time[1]}', f'{new_end_time[0]}' + ':' + f'{new_end_time[1]}']
                        break

                new_time = [new_time[0], new_time[1] + 15]
                if new_time[1] > 45:
                    new_time[0] += 1
                    new_time[1] = 0
                        
#Stoliki alternatywne
        for i in range(5):
            search_further = True
            stolik = Stolik_item.objects.get(stolik_miejsca = i + 1)
            if stolik.stolik_miejsca == self.stolik.stolik_miejsca:
                continue
            
            r = Reservation.objects.filter(rezerwacja_dzien = self.day, stolik = stolik)
            for j, d in enumerate(r):
                self.save_begin, self.save_end = None, None
                s1, s2, s3, s4 = 2, 2, 2, 2
                l1 = d.time_begin.find(':')
                l2 = d.time_end.find(':')
                le1 = len(d.time_begin)
                le2 = len(d.time_end)
                if l1 < 2:
                    s1 = 1
                if le1 + (2 - s1) < 5:
                    s2 = 1
                if l2 < 2:
                    s3 = 1
                if le2 + (2 - s3) < 5:
                    s4 = 1
                for k, time in enumerate(self.times_table[i]):
                    if time[0] == int(d.time_begin[0:s1]) and time[1] == int(d.time_begin[-s2:]):
                        self.save_begin = k
                    elif time[0] == int(d.time_end[0:s3]) and time[1] == int(d.time_end[-s4:]):
                        self.save_end = k + 1

                if self.save_begin is not None and self.save_end is not None:
                    del self.times_table[i][self.save_begin:self.save_end]

            if self.begin_time in self.times_table[i] and self.end_time in self.times_table[i]:
                self.alternatives[i] = [i+1, 'Stolik dostępny na wybrany termin', f'{self.begin_time[0]}' + ':' + f'{self.begin_time[1]}', f'{self.end_time[0]}' + ':' + f'{self.end_time[1]}']
                continue
            elif self.begin_time in self.times_table[i]:
                start, success = True, False
                new_time = None
                new_time = [self.end_time[0], self.end_time[1] - 15]
                if new_time[1] < 0:
                    new_time[0] -= 1
                    new_time[1] = 45
                while(start):
                    if new_time[0] < self.begin_time[0] or new_time[0] == self.begin_time[0] and new_time[1] <= self.begin_time[1]:
                        start = False
                        break
                    if new_time in self.times_table[i]:
                        start=False
                        success = True
                        break
                    new_time = [new_time[0], new_time[1] - 15]
                    if new_time[1] < 0:
                        new_time[0] -= 1
                        new_time[1] = 45

                if success:
                    h = (new_time[0]*60 + new_time[1]) - (self.begin_time[0] * 60 + self.begin_time[1])
                    if h >= 45:
                        self.alternatives[i] = [i+1, f'Możliwa rezerwacja na wybrany termin na {h} minut\n zamiast na {self.time_in_minutes} minut',\
                            f'{self.begin_time[0]}' + ':' + f'{self.begin_time[1]}', f'{new_time[0]}' + ':' + f'{new_time[1]}']
                        search_further = True

            if search_further:
                start = True
                new_time = [self.begin_time[0], self.begin_time[1] + 15]
                if new_time[1] > 45:
                    new_time[0] += 1
                    new_time[1] = 0
                while(start):
                    if new_time[0] > 21:
                        start = False
                        self.alternatives[i] = [i+1, f'Brak możliwości na dany dzień', '0', '0']
                        break
                    if new_time in self.times_table[i]:
                        new_end_time = [new_time[0], new_time[1] + 45]
                        if new_end_time[1] > 45:
                            new_end_time[0] += 1
                            new_end_time[1] = np.mod(new_time[1] + 45, 60)
                        nonstop, success = True, True
                        while(nonstop):
                            if new_end_time in self.times_table[i]:
                                if (new_end_time[0]*60 + new_end_time[1]) - (new_time[0]*60 + new_time[1]) == self.time_in_minutes:
                                    nonstop = False
                                    break
                                new_end_time = [new_end_time[0], new_end_time[1] + 15]
                                if new_end_time[1] > 45:
                                    new_end_time[0] += 1
                                    new_end_time[1] = 0
                                continue

                            if new_end_time[0]*60 + new_end_time[1] == new_time[0]*60 + new_time[1] + 45:
                                success = False

                            nonstop = False
                            break

                        if success:
                            time = (new_end_time[0]*60 + new_end_time[1]) - (new_time[0]*60 + new_time[1])
                            if time == self.time_in_minutes:
                                self.alternatives[i] = [i+1, f'Możliwa rezerwacja na godzine {new_time[0]}:{new_time[1]} na {time} minut',\
                                    f'{new_time[0]}' + ':' + f'{new_time[1]}', f'{new_end_time[0]}' + ':' + f'{new_end_time[1]}']
                            else:
                                self.alternatives[i] = [i+1, f'Możliwa rezerwacja na godzine {new_time[0]}:{new_time[1]} na {time} minut\n zamiast na {self.time_in_minutes} minut',\
                                    f'{new_time[0]}' + ':' + f'{new_time[1]}', f'{new_end_time[0]}' + ':' + f'{new_end_time[1]}']
                            break
                       
                    new_time = [new_time[0], new_time[1] + 15]
                    if new_time[1] > 45:
                        new_time[0] += 1
                        new_time[1] = 0

        return self.alternatives
            
@login_required
def reservation(request):
    dates = {'min': date.today().strftime('%Y-%m-%d'), 'max': (date.today() + timedelta(days=10)).strftime('%Y-%m-%d')}
    sug = {'suc': '', 'alt1': {}, 'alt2': {}, 'alt3': {}, 'alt4': {}, 'alt5': {}}
    short = ['alt' + str(i+1) for i in range(5)]
    colors = []
    form2 = None
    if request.method == 'POST':
        if 'date_submit' in request.POST:
            form = ReservationForm(request.POST)
            if form.is_valid():
                seats = form.cleaned_data['places_by_table']
                try:
                    time_begin = form.cleaned_data['time_begin']
                    time_end = form.cleaned_data['time_end']
                    day = form.cleaned_data['day']
                except:
                    messages.error(request, 'Błąd w terminie')
                    AllActions.objects.create(user=request.user, action_id=23, action="Rezerwacja: źle podany termin")
                    return redirect('reservation1')
                begin_h = time_begin.hour
                begin_m = time_begin.minute
                end_h = time_end.hour
                end_m = time_end.minute
                err = (end_h * 60 + end_m) - (begin_h * 60 + begin_m)
                #if day < date.today():
                #    messages.error(request, f'Nie można wykonać rezerwacji na datę przeszłą :)')        #włączyć na produkcję
                #    AllActions.objects.create(user=request.user, action_id=10, action="Rezerwacja: podano przeeszłą datę")
                #    return redirect('reservation1')
                overpay = None
                if err < 0: 
                    messages.error(request, f'Zakończenie rezerwacji nie może wypaść przed jej rozpoczęciem :)')
                    AllActions.objects.create(user=request.user, action_id=9, action="Rezerwacja: godzina zakończenia wcześniej od daty rozpoczęcia")
                    return redirect('reservation1')
                if err < 45:
                    messages.error(request, f'Minimalny czas rezerwacji to 45 minut - podano {err} minut')
                    AllActions.objects.create(user=request.user, action_id=11, action="Rezerwacja: podano za krótki czas rezerwacji")
                    return redirect('reservation1')

                if err > 90 and err < 150:
                    overpay = 90 * int(seats)
                    messages.warning(request, f'Przy rezerwacji o czasie przekraczającym 1.5h minimalny koszt rezerwacji musi wynieść co najmniej {overpay} zł')
                    AllActions.objects.create(user=request.user, action_id=12, action='Rezerwacja: rezerwacja przekraczająca 1.5h')

                elif err >= 150 and err < 210:
                    overpay = 150 * int(seats)
                    messages.warning(request, f'Przy rezerwacji o czasie przekraczającym 2.5h minimalny koszt rezerwacji musi wynieść co najmniej {overpay} zł')
                    AllActions.objects.create(user=request.user, action_id=13, action='Rezerwacja: rezerwacja przekraczająca 2.5h')

                elif err >= 210 and err <= 270:
                    overpay = 275 * int(seats)
                    messages.warning(request, f'Przy rezerwacji o czasie przekraczającym 3.5h minimalny koszt rezerwacji musi wynieść co najmniej {overpay} zł')
                    AllActions.objects.create(user=request.user, action_id=14, action='Rezerwacja: rezerwacja przekraczająca 3.5h')

                elif err > 270:
                    messages.warning(request, 'Dla rezerwacji powyżej 4.5h prosimy skontaktować się z obsługą restauracji')
                    AllActions.objects.create(user=request.user, action_id=15, action='Rezerwacja: rezerwacja przekraczająca 4.5h')
                    return redirect('reservation1')

                request.session['cena'] = overpay
                table = Stolik_item.objects.get(stolik_miejsca = seats)
                temp_reservations = list(Temp_Reservation.objects.filter(rezerwacja_dzien = day, stolik = table))
                reservations = Reservation.objects.filter(rezerwacja_dzien = day, stolik = table)
                for reservation in reservations:
                    obj = Helper_class(table, request.user, day, reservation.time_begin, reservation.time_end)
                    temp_reservations.append(obj)
                ad = AvailableDate([begin_h, begin_m], [end_h, end_m], day, temp_reservations, table)
                suggestions = ad.return_accept()

                if suggestions == 'reserve':
                    strg = 'alt' + seats
                    sug['suc'] = 'reserve'
                    sug[strg] = 1
                    res = Temp_Reservation.objects.create(nazwa=request.user, rezerwacja_dzien=day.strftime('%Y-%m-%d'), time_begin=f'{begin_h}' + ':' + f'{begin_m}', time_end=f'{end_h}' + ':' + f'{end_m}')
                    res.stolik.add(table)
                    res.save()
                    request.session['res_made'] = True
                    return redirect('reservation2')

                else:
                    request.session['day'] = datetime.strftime(day, '%Y-%m-%d')
                    sug['suc'] = 'ayy'
                    temp_text = []
                    for i in range(len(suggestions)):
                        if suggestions[i][1] == 'Brak możliwości na dany dzień':
                            continue

                        if suggestions[i][1] == 'Stolik dostępny na wybrany termin':
                            colors.append('#CCFFCC')
                        else:
                            colors.append('#FF6666')
                        temp_text.append(suggestions[i][1])
                        sug[short[i]] = {'first': suggestions[i][0], 'second': suggestions[i][1]}
                        request.session[short[i]] = {'first': suggestions[i][2], 'second': suggestions[i][3]}
                    suggestions = np.array(suggestions)
                    ch = list(zip([i+1 for i in range(len(sug.keys()))], temp_text))
                    form2 = PickForm(choice = ch)
        elif 'place_submit' in request.POST:
            form2 = PickForm(request.POST)
            if form2.is_valid():
                strg = 'alt' + form2.cleaned_data['choice']
                table = Stolik_item.objects.get(stolik_miejsca=form2.cleaned_data['choice'])
                res = Temp_Reservation.objects.create(nazwa=request.user, rezerwacja_dzien=request.session['day'], time_begin=request.session[strg]['first'], time_end=request.session[strg]['second'])
                res.stolik.add(table)
                res.save()
                AllActions.objects.create(user=request.user, action_id=16, action="Rezerwacja: pomyślny wybór daty i stolika")
                return redirect('reservation2')

    else:
        form = ReservationForm()

    return render(request, 'reservation/rezerwacje.html', {'form_res':form, 'form2': form2, 'sugg':sug, 'colors': colors, 'dates': dates})

@login_required
def reservation_items(request):
    return render(request, 'reservation/rezerwacje_jedzenie.html')

from .models import Skladnik
from .models import Menu_item
from .models import Menu_org

def skladnik_item(request):
    obj=Skladnik.objects.all()
    return render(request,"reservation/skladniki.html",{'obj':obj})


def menu_items(request):
    menu_items=Menu_item.objects.all()
    return render(request,"reservation/rezerwacje_jedzenie.html",{'menu_items':menu_items})

@login_required
def rezerwacje_dodaj_zamowienie(request):
    breakpoint()
    try:
        rezerwacja_stolika_temp=Temp_Reservation.objects.get(nazwa=request.user)
    except:
        return redirect('reservation1')
    cena=0.0
    cena=Decimal(cena)
    dane_rezerwacji=rezerwacja_stolika_temp
    menu_orgs=Menu_org.objects.all()
    try:
        obecna_sesja=Tymczasowe_zamowienie.objects.get(nazwa_uzytkownika=request.user)
    except:
        obecna_sesja=Tymczasowe_zamowienie.objects.create(nazwa_uzytkownika=request.user)
    if request.method=="POST":
        if 'przycisk_rezygnacja' in request.POST:
            obecna_sesja.delete()
            return redirect('reservation2')
        form=zamowienie_tymczasowe(request.POST)
        form2=dodaj_edytowane_danie(request.POST)
        if form2.is_valid():
            for pojedyncze_menu in menu_orgs:
                for elementu_pojedynczego_menu in pojedyncze_menu.zawartosc.all():
                    try:
                        if(request.POST[elementu_pojedynczego_menu.nazwa]=='dodaj'):
                            item_orginalny_z_menu=Menu_item.objects.get(nazwa=elementu_pojedynczego_menu.nazwa)
                            nowy_element_zamowienia=Produkt_rezerwacji.objects.create(nazwa_produktu=item_orginalny_z_menu)
                            obecna_sesja.zamowienie_item.add(nowy_element_zamowienia)
                    except:
                        pass
            for itemy_zamowienia in obecna_sesja.zamowienie_item.all():
                try:
                    if(request.POST[str(itemy_zamowienia)]=='edytuj'):
                        do_edycji=Produkt_rezerwacji.objects.get(pk=itemy_zamowienia.pk)
                        obecna_sesja.tymczasowe_edytowane.clear()
                        obecna_sesja.tymczasowe_edytowane.add(do_edycji)
                        return redirect('reservation2_edit')
                    elif(request.POST[str(itemy_zamowienia)]=='usun'):
                         do_usuniecia=Produkt_rezerwacji.objects.get(pk=itemy_zamowienia.pk)
                         do_usuniecia.delete()

                except:
                    pass
        print(request.body)
        komentarz_do_zamowienia=request.POST.get('komentarz_do_zamowienia')
        if('akceptuj_przycisk'in request.POST):
            for dania in obecna_sesja.zamowienie_item.all():
                cena=cena+dania.nazwa_produktu.cena
                for skladnik_w_daniu in dania.dodaj_skladnik.all():
                    cena=cena+skladnik_w_daniu.cena
            Rezerwacja=Reservation.objects.create(nazwa = request.user,cena_rachunek=cena,rezerwacja_dzien = rezerwacja_stolika_temp.rezerwacja_dzien,time_begin = rezerwacja_stolika_temp.time_begin,time_end = rezerwacja_stolika_temp.time_end,czas_rezerwacji = rezerwacja_stolika_temp.czas_rezerwacji,aktywnosc=True)
            print(rezerwacja_stolika_temp.stolik.all().first())
            Rezerwacja.stolik.add(rezerwacja_stolika_temp.stolik.all().first())
            for itemki_zamowienia in obecna_sesja.zamowienie_item.all():
                Rezerwacja.zamowienie_item.add(itemki_zamowienia)
            Rezerwacja.save()
            obecna_sesja.delete()
            rezerwacja_stolika_temp.delete()
            return redirect('home')
            #return redirect('moje_rezerwacje')
    else:
        form=Tymczasowe_zamowienie()
        form2=dodaj_edytowane_danie()
    cena=0.0
    cena=Decimal(cena)
    for dania in obecna_sesja.zamowienie_item.all():
        cena=cena+dania.nazwa_produktu.cena
        for skladnik_w_daniu in dania.dodaj_skladnik.all():
            cena=cena+skladnik_w_daniu.cena
    return render(request,'reservation/rezerwacje_jedzenie.html',{'form':form,'menu_orgs':menu_orgs,'obecna_sesja':obecna_sesja.zamowienie_item,'form2':form2,'cena_zamowienia':cena,'dane_rezerwacji':dane_rezerwacji})


@login_required
def edycja_dania(request):
    try:
        rezerwacja_stolika_temp=Temp_Reservation.objects.get(nazwa=request.user)
    except:
        return redirect('reservation1')
    wszystkie_skladniki=Skladnik.objects.all()
    try:
        obecna_sesja=Tymczasowe_zamowienie.objects.get(nazwa_uzytkownika=request.user)
        obecna_sesja.tymczasowe_edytowane.last().nazwa_produktu
        edytowany_item=obecna_sesja.tymczasowe_edytowane.last()
    except:
        return redirect('reservation2')
    dane_rezerwacji=rezerwacja_stolika_temp
    produkt_z_menu=obecna_sesja.tymczasowe_edytowane.last()
    print(produkt_z_menu.nazwa_produktu)
    print(wszystkie_skladniki.all())
    jakie_mozna_dodac=wszystkie_skladniki.all()
    edytowany_item=obecna_sesja.tymczasowe_edytowane.last()
    if request.method=="POST":
        for skladnik in wszystkie_skladniki.all():
                try:
                    if(request.POST[str(skladnik)]=='dodaj'):
                        dodaj=True
                        for zabrane in edytowany_item.odejmij_skladnik.all():
                            if (zabrane==skladnik):
                                edytowany_item.odejmij_skladnik.remove(skladnik)
                        for dodane in edytowany_item.dodaj_skladnik.all():
                            if(skladnik==dodane):
                                dodaj=False
                        for skladniki_dania in edytowany_item.nazwa_produktu.skladniki.all():
                            if(str(skladniki_dania)==str(skladnik)):
                                dodaj=False
                        if(dodaj==True):
                            dodawany=Skladnik.objects.get(nazwa=skladnik.nazwa)
                            edytowany_item.dodaj_skladnik.add(dodawany)
                    if(request.POST[str(skladnik)]=='odejmij'):
                        for dodane in edytowany_item.dodaj_skladnik.all():
                            if (dodane==skladnik):
                                edytowany_item.dodaj_skladnik.remove(skladnik)
                        for skladniki_dania in produkt_z_menu.skladniki.all():
                            if(skladnik==skladniki_dania):
                                odejmowany=Skladnik.objects.get(nazwa=skladnik.nazwa)
                                edytowany_item.odejmij_skladnik.add(odejmowany)
                except:
                    pass
                for itemy_zamowienia in obecna_sesja.zamowienie_item.all():
                    try:
                        if(request.POST[str(itemy_zamowienia)]=='edytuj'):
                            do_edycji=Produkt_rezerwacji.objects.get(pk=itemy_zamowienia.pk)
                            obecna_sesja.tymczasowe_edytowane.clear()
                            obecna_sesja.tymczasowe_edytowane.add(do_edycji)
                            return redirect('reservation2_edit')
                        elif(request.POST[str(itemy_zamowienia)]=='usun'):
                             do_usuniecia=Produkt_rezerwacji.objects.get(pk=itemy_zamowienia.pk)
                             do_usuniecia.delete()
                             return redirect('reservation2')

                    except:
                        pass
        if('zakoncz_edycje_dania'in request.POST):
            return redirect('reservation2')
    else:
        pass
    cena=0.0
    cena=Decimal(cena)
    for dania in obecna_sesja.zamowienie_item.all():
        cena=cena+dania.nazwa_produktu.cena
        for skladnik_w_daniu in dania.dodaj_skladnik.all():
            cena=cena+skladnik_w_daniu.cena
    return render(request,'reservation/edytowane.html',{'obecna_sesja':obecna_sesja.zamowienie_item,'cena_zamowienia':cena,'skladniki_edytowanego':obecna_sesja.tymczasowe_edytowane.first().nazwa_produktu.skladniki,'wszystkie_skladniki':wszystkie_skladniki,'dane_rezerwacji':dane_rezerwacji,'skladniki_dodane':obecna_sesja.tymczasowe_edytowane.first().dodaj_skladnik})
