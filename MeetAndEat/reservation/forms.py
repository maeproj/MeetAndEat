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

    places_by_table = forms.ChoiceField(choices=PLACE_CHOICES, widget=forms.RadioSelect(attrs={'style': 'list-style:none; padding:0; margin:0;'}))

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
        self.fields['choice'] = forms.ChoiceField(label='Możliwości', choices=CHOICES, widget=forms.RadioSelect)

    class Meta:
        model = User
        fields = ['choice']


