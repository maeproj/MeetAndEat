from django.contrib.auth.models import models, User
from django.contrib.auth.forms import UserCreationForm
from django import forms
from .models import Reservation
from copy import deepcopy
from datetime import timedelta, date

class ReservationForm(forms.Form):
    PLACE_CHOICES = [(1, 'Jedno'),
               (2, 'Dwa'),
               (3, 'Trzy'),
               (4, 'Cztery'),
               (5, 'Piec')]
    BEGIN_CHOICES_H = [(16, '16'),
                       (17, '17'),
                       (18, '18'),
                       (19, '19'),
                       (20, '20'),
                       (21, '21')]
    BEGIN_CHOICES_M = [(0, '00'),
                       (15, '15'),
                       (30, '30'),
                       (45, '45')]
    END_CHOICES_H = [(16, '16'),
                     (17, '17'),
                     (18, '18'),
                     (19, '19'),
                     (20, '20'),
                     (21, '21')]
    END_CHOICES_M = [(0, '00'),
                     (15, '15'),
                     (30, '30'),
                     (45, '45')]
    places_by_table = forms.ChoiceField(choices=PLACE_CHOICES, widget=forms.RadioSelect)
    #day = forms.DateField(widget=DatePickerInput(format='%d-%m-%Y'))
    day = forms.DateField(widget=forms.DateInput(attrs = {'input_type': 'date'}))
    begin_h = forms.IntegerField(widget=forms.Select(choices=BEGIN_CHOICES_H))
    begin_m = forms.IntegerField(widget=forms.Select(choices=BEGIN_CHOICES_M))
    end_h = forms.IntegerField(widget=forms.Select(choices=END_CHOICES_H))
    end_m = forms.IntegerField(widget=forms.Select(choices=END_CHOICES_M))
    #time_begin = forms.TimeField(widget=TimePickerInput())
    #time_end = forms.TimeField(widget=TimePickerInput())

    class Meta:
        model = User
        fields = ['places_by_table', 'day', 'begin_h', 'begin_m', 'end_h', 'end_m']
        #fields = ['places_by_table', 'day', 'time_begin', 'time_end']


