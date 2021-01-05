from django import forms
from django.conf import settings
from django.contrib.auth.hashers import check_password
from django.contrib.auth.models import models, User
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.backends import BaseBackend
from datetime import date
from .models import NewUser
from phonenumber_field.formfields import PhoneNumberField

class UserRegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)
    telefon = PhoneNumberField()

    def __init__(self, *args, **kwargs):
        super(UserRegisterForm, self).__init__(*args, **kwargs)
        self.fields['password1'].help_text = 'Hasło powinno zawierać: <ul><li>Co najmniej 8 znaków</li><li>Co najmniej jedną wielką literę</li>\
        <li>Co najmniej jeden znak specjalny ./@/#/$/^/&</li><li>Co najmniej jedną cyfrę</li></ul>'

    class Meta:
        model = User
        fields = ['username', 'first_name', 'email', 'telefon', 'password1', 'password2']

class UserLoginForm(forms.Form):
    username = forms.CharField(label='Login', max_length=100)
    password = forms.CharField(label='Hasło', max_length=100)

    class Meta:
        model = User
        fields = ['username', 'password']

class ChangePassClick(forms.Form):
    btn = forms.IntegerField()


    
