from django.contrib.auth.models import models, User
from django.contrib.auth.forms import UserCreationForm
from django import forms
from .models import Reservation,Produkt_rezerwacji,Tymczasowe_zamowienie,Menu_item
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

    places_by_table = forms.ChoiceField(choices=PLACE_CHOICES, widget=forms.RadioSelect())
    day = forms.DateField(widget=DatePickerInput(attrs={'type': "date", 'name': "dzien", 'min': date.today().strftime('%Y-%m-%d'), 'max': (date.today() + timedelta(days=10)).strftime('%Y-%m-%d')}))
    time_begin = forms.TimeField(widget=TimePickerInput(attrs={'type': "time", 'name': "czas-start", 'step': "900", 'min': "16:00:00", 'max': "21:45:00"}))
    time_end = forms.TimeField(widget=TimePickerInput(attrs={'type': "time", 'name': "czas-start", 'step': "900", 'min': "16:00:00", 'max': "21:45:00"}))

    class Meta:
        model = User
        fields = ['places_by_table', 'day', 'time_begin', 'time_end']

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

class dodaj_dania_do_rezerwacji(forms.ModelForm):
    class Meta:
        model=Reservation
        fields=['cena_rachunek','komentarz']


class dodaj_edytowane_danie(forms.ModelForm):
    class Meta:
        model=Produkt_rezerwacji
        fields= ('nazwa_produktu','dodaj_skladnik','odejmij_skladnik','podanie_godzina','podanie_minuta')
        def __init__(self, *args, **kwargs):
            super(dodaj_edytowane_danie, self).__init__(*args, **kwargs)
            self.fields["nazwa_produktu"].widget = forms.CheckboxSelectMultiple()
            self.fields["nazwa_produktu"].queryset = Menu_item.objects.all()
        
class zamowienie_tymczasowe(forms.ModelForm):
    class Meta:
        model=Tymczasowe_zamowienie
        fields=['zamowienie_item']


