from django.contrib.auth.models import models, User
from django.contrib.auth.forms import UserCreationForm
from django import forms
from bootstrap_datepicker_plus import DatePickerInput, TimePickerInput
from .models import Reservation
from copy import deepcopy
from datetime import timedelta, date

class ReservationForm(forms.Form):
    PLACE_CHOICES = [('1', 'Jedno'),
               ('2', 'Dwa'),
               ('3', 'Trzy'),
               ('4', 'Cztery'),
               ('5', 'Piec')]
    BEGIN_CHOICES_H = [('16', '16'),
                       ('17', '17'),
                       ('18', '18'),
                       ('19', '19'),
                       ('20', '20'),
                       ('21', '21')]
    BEGIN_CHOICES_M = [('0', '00'),
                       ('15', '15'),
                       ('30', '30'),
                       ('45', '45')]
    END_CHOICES_H = [('16', '16'),
                     ('17', '17'),
                     ('18', '18'),
                     ('19', '19'),
                     ('20', '20'),
                     ('21', '21')]
    END_CHOICES_M = [('0', '00'),
                     ('15', '15'),
                     ('30', '30'),
                     ('45', '45')]
    places_by_table = forms.ChoiceField(choices=PLACE_CHOICES, widget=forms.RadioSelect)
    #day = forms.DateField(widget=DatePickerInput(format='%d-%m-%Y'))
    dat = forms.DateField(widget=forms.DateInput(attrs={'onchange': 'submit();'}))
    begin_h = forms.CharField(widget=forms.Select(choices=BEGIN_CHOICES_H))
    begin_m = forms.CharField(widget=forms.Select(choices=BEGIN_CHOICES_M))
    end_h = forms.CharField(widget=forms.Select(choices=END_CHOICES_H))
    end_m = forms.CharField(widget=forms.Select(choices=END_CHOICES_M))
    #time_begin = forms.TimeField(widget=TimePickerInput())
    #time_end = forms.TimeField(widget=TimePickerInput())

    class Meta:
        model = User
        fields = ['places_by_table', 'day', 'begin_h', 'begin_m', 'end_h', 'end_m']
        #fields = ['places_by_table', 'day', 'time_begin', 'time_end']

class AvailableDate:
    def __init__(self, date, stolik):
        self.times = [(16, 0),
                      (16, 15),
                      (16, 30),
                      (16, 45),
                      (17, 0),
                      (17, 15),
                      (17, 30),
                      (17, 45),
                      (18, 0),
                      (18, 15),
                      (18, 30),
                      (18, 45),
                      (19, 0),
                      (19, 15),
                      (19, 30),
                      (19, 45),
                      (20, 0),
                      (20, 15),
                      (20, 30),
                      (20, 45),
                      (21, 0),
                      (21, 15),
                      (21, 30),
                      (21, 45)]
        self.dates = []
        for i in range(30):
            self.dates.append([date.today() + timedelta(days=i), ])
        self.res = Reservation.objects.get(rezerwacja_dzien = date, stolik = stolik)
        self.save_begin = None
        self.save_end = None

        for d in self.res:
            for i, time in enumerate(self.times):
                if time[0] == d.begin_h and time[1] == d.begin_m:
                    self.save_begin = i
                elif time[0] == d.end_h and time[1] == d.end_m:
                    self.save_end = i

            del self.times[self.save_begin:self.save_end]

    def return_dates(self):
        return self.times


