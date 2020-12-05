from django.contrib.auth.models import models, User
from django.contrib.auth.forms import UserCreationForm
from django import forms
from bootstrap_datepicker_plus import DatePickerInput, TimePickerInput

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
    BEGIN_CHOICES_M = [(1, '00'),
                       (15, '15'),
                       (30, '30'),
                       (45, '45')]
    END_CHOICES_H = [(16, '16'),
                     (17, '17'),
                     (18, '18'),
                     (19, '19'),
                     (20, '20'),
                     (21, '21')]
    END_CHOICES_M = [(1, '00'),
                     (15, '15'),
                     (30, '30'),
                     (45, '45')]
    places_by_table = forms.ChoiceField(choices=PLACE_CHOICES, widget=forms.RadioSelect)
    day = forms.DateField(widget=DatePickerInput(format='%d-%m-%Y'))
    #begin_h = forms.CharField(widget=forms.Select(choices=BEGIN_CHOICES_H))
    #begin_m = forms.CharField(widget=forms.Select(choices=BEGIN_CHOICES_M))
    #end_h = forms.CharField(widget=forms.Select(choices=END_CHOICES_H))
    #end_m = forms.CharField(widget=forms.Select(choices=END_CHOICES_M))
    time_begin = forms.TimeField(widget=TimePickerInput())
    time_end = forms.TimeField(widget=TimePickerInput())

    class Meta:
        model = User
        #fields = ['places_by_table', 'day', 'begin_h', 'begin_m', 'end_h', 'end_m']
        fields = ['places_by_table', 'day', 'time_begin', 'time_end']


