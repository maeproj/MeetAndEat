from django.shortcuts import render, redirect
from django.http import HttpResponse
from .forms import ReservationForm, PickForm
from django.contrib.auth.decorators import login_required
from datetime import date, time, datetime, timedelta
from django.contrib import messages
from .models import Reservation, Stolik_item
from copy import deepcopy
import numpy as np
import pdb
from global_modules.models import AllActions

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
        self.alternatives = [(0, 0), (0, 0), (0, 0), (0, 0), (0, 0)]
        self.save_begin = None
        self.save_end = None
        for d in self.res:
            self.save_begin, self.save_end = None, None
            for i, time in enumerate(self.times):
                if time[0] == int(d.begin_h) and time[1] == int(d.begin_m):
                    self.save_begin = i
                elif time[0] == int(d.end_h) and time[1] == int(d.end_m):
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
                    self.alternatives[self.stolik.stolik_miejsca - 1] = [self.stolik.stolik_miejsca, f'Możliwa rezerwacja na wybrany termin na {h} minut zamiast na {self.time_in_minutes} minut']
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
                    self.alternatives[self.stolik.stolik_miejsca - 1] = [self.stolik.stolik_miejsca, f'Brak możliwości na dany dzień']
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
                            self.alternatives[self.stolik.stolik_miejsca - 1] = [self.stolik.stolik_miejsca, f'Możliwa rezerwacja na godzine {new_time[0]}:{new_time[1]} na {time} minut']
                        else:
                            self.alternatives[self.stolik.stolik_miejsca - 1] = [self.stolik.stolik_miejsca, f'Możliwa rezerwacja na godzine {new_time[0]}:{new_time[1]} na {time} minut\n zamiast na {self.time_in_minutes} minut']
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
                for k, time in enumerate(self.times_table[i]):
                    if time[0] == int(d.begin_h) and time[1] == int(d.begin_m):
                        self.save_begin = k
                    elif time[0] == int(d.end_h) and time[1] == int(d.end_m):
                        self.save_end = k + 1

                if self.save_begin is not None and self.save_end is not None:
                    del self.times_table[i][self.save_begin:self.save_end]

            if self.begin_time in self.times_table[i] and self.end_time in self.times_table[i]:
                self.alternatives[i] = [i+1, 'Stolik dostępny na wybrany termin']
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
                        self.alternatives[i] = [i+1, f'Możliwa rezerwacja na wybrany termin na {h} minut\n zamiast na {self.time_in_minutes} minut']
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
                        self.alternatives[i] = [i+1, f'Brak możliwości na dany dzień']
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
                                self.alternatives[i] = [i+1, f'Możliwa rezerwacja na godzine {new_time[0]}:{new_time[1]} na {time} minut']
                            else:
                                self.alternatives[i] = [i+1, f'Możliwa rezerwacja na godzine {new_time[0]}:{new_time[1]} na {time} minut\n zamiast na {self.time_in_minutes} minut']
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
    form2 = None
    if request.method == 'POST':
        if 'date_submit' in request.POST:
            form = ReservationForm(request.POST)
            if form.is_valid():
                #day = form.cleaned_data['day']
                seats =form.cleaned_data['places_by_table']
                #time_begin = form.cleaned_data['time_begin']
                #time_end = form.cleaned_data['time_end']
                time_begin = datetime.strptime(request.POST.get('czas-start'), '%H:%M').time()
                time_end = datetime.strptime(request.POST.get('czas-koniec'), '%H:%M').time()
                day = datetime.strptime(request.POST.get('dzien'), '%Y-%m-%d').date()
                begin_h = time_begin.hour
                begin_m = time_begin.minute
                end_h = time_end.hour
                end_m = time_end.minute
                err = (end_h * 60 + end_m) - (begin_h * 60 + begin_m)
                #if day < date.today():
                #    messages.error(request, f'Nie można wykonać rezerwacji na datę przeszłą :)')        #włączyć na produkcję
                #    AllActions.objects.create(user=request.user, action_id=10, action="Rezerwacja: podano przeeszłą datę")
                #    return redirect('reservation1')
                if err < 0: 
                    messages.error(request, f'Zakończenie rezerwacji nie może wypaść przed jej rozpoczęciem :)')
                    AllActions.objects.create(user=request.user, action_id=9, action="Rezerwacja: godzina zakończenia wcześniej od daty rozpoczęcia")
                    return redirect('reservation1')
                if err < 45:
                    messages.error(request, f'Minimalny czas rezerwacji to 45 minut - podano {err} minut')
                    AllActions.objects.create(user=request.user, action_id=11, action="Rezerwacja: podano za krótki czas rezerwacji")
                    return redirect('reservation1')

                table = Stolik_item.objects.get(stolik_miejsca = seats)
                reservations = Reservation.objects.filter(rezerwacja_dzien = day, stolik = table)
                ad = AvailableDate([begin_h, begin_m], [end_h, end_m], day, reservations, table)
                suggestions = ad.return_accept()

                if suggestions == 'reserve':
                    sug['suc'] = 'reserve'
                else:
                    sug['suc'] = 'ayy'
                    for i in range(len(suggestions)):
                        sug[short[i]] = {'first': suggestions[i][0], 'second': suggestions[i][1]}
                        request.session[short[i]] = suggestions[i][1]
                    suggestions = np.array(suggestions)
                    ch = list(zip([i+1 for i in range(5)], suggestions[:, 1]))
                    form2 = PickForm(choice = ch)
            elif 'place_submit' in request.POST:
                form2 = PickForm(request.POST)
                if form2.is_valid():
                    AllActions.objects.create(user=request.user, action_id=12, action="Rezerwacja: pomyślny wybór daty i stolika")
                    return redirect('reservation2')

    else:
        form = ReservationForm()
    return render(request, 'reservation/rezerwacje.html', {'form':form, 'form2': form2, 'sugg':sug, 'dates': dates})

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


def menu_orgs(request):
    menu_orgs=Menu_org.objects.all()
    return render(request,"reservation/rezerwacje_jedzenie.html",{'menu_orgs':menu_orgs})