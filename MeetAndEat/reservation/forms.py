from django.contrib.auth.models import models, User
from django.contrib.auth.forms import UserCreationForm
from django import forms
from .models import Reservation
from copy import deepcopy
from datetime import timedelta, date, datetime
from bootstrap_datepicker_plus import TimePickerInput, DatePickerInput

class DateInput(forms.DateInput):
    input_type = 'date'

class TimeInput(forms.TimeInput):
    input_type = 'time'

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

    class Meta:
        model = User
        fields = ['places_by_table']

class PickForm(forms.Form):
    CHOICES = []
    def __init__(self, *args, **kwargs):
        try:
            CHOICES = kwargs.pop('choice')
        except:
            CHOICES = [(1,1), (2,2), (3,3), (4,4), (5,5)]
        super(PickForm, self).__init__(*args, **kwargs)
        self.fields['choice'] = forms.ChoiceField(choices=CHOICES, widget=forms.RadioSelect)

    class Meta:
        model = User
        fields = ['choice']


