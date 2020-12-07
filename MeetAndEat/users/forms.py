from django import forms
from django.conf import settings
from django.contrib.auth.hashers import check_password
from django.contrib.auth.models import models, User
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.backends import BaseBackend
from datetime import date
from .models import NewUser

class UserRegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['username', 'first_name', 'email', 'password1', 'password2']

class UserLoginForm(forms.Form):
    username = forms.CharField(label='Login', max_length=100)
    password = forms.CharField(label='Hasło', max_length=100)

    class Meta:
        model = User
        fields = ['username', 'password']


    
