from django import forms
from django.conf import settings
from django.contrib.auth.hashers import check_password
from django.contrib.auth.models import models, User
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.backends import BaseBackend
from datetime import date
from .models import NewUser
from phonenumber_field.formfields import PhoneNumberField
from phonenumbers import PhoneNumber
from django.contrib.auth.forms import PasswordChangeForm

class UserRegisterForm(UserCreationForm):
    email = forms.EmailField(label='', required=True, widget=forms.EmailInput(attrs = {'type': 'text', 'class': 'rejestracja_input', 'placeholder': 'Email', 'onfocus': "this.placeholder=''", 'onblur': "this.placeholder='Email'"}))
    telefon = PhoneNumberField(label='')
    telefon.widget.build_attrs({'type': PhoneNumber}, extra_attrs={'class': 'rejestracja_input', 'placeholder': 'Telefon', 'onfocus': "this.placeholder=''", 'onblur': "this.placeholder='Telefon'"})
    def __init__(self, *args, **kwargs):
        super(UserRegisterForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs = {'class': 'rejestracja_input', 'placeholder': 'Nickname', 'onfocus': "this.placeholder=''", 'onblur': "this.placeholder='Nickname'"}
        self.fields['password1'].widget.attrs = {'class': 'rejestracja_input', 'placeholder': 'Hasło', 'onfocus': "this.placeholder=''", 'onblur': "this.placeholder='Hasło'"}
        self.fields['first_name'].widget.attrs = {'class': 'rejestracja_input', 'placeholder': 'Imię', 'onfocus': "this.placeholder=''", 'onblur': "this.placeholder='Imię'"}
        self.fields['password2'].widget.attrs = {'class': 'rejestracja_input', 'placeholder': 'Powtórz hasło', 'onfocus': "this.placeholder=''", 'onblur': "this.placeholder='Powtórz hasło'"}
        self.fields['password1'].help_text = '<div></br></div>Hasło powinno zawierać: <ul style="list-style:none; padding:0; margin:0;"><li>Co najmniej 8 znaków</li><li>Co najmniej jedną wielką literę</li>\
        <li>Co najmniej jeden znak specjalny ./_/@/#/^/&</li><li>Co najmniej jedną cyfrę</li></ul></br>'
        self.fields['username'].label = ''
        self.fields['password1'].label = ''
        self.fields['password2'].label = ''
        self.fields['first_name'].label = ''
        self.fields['username'].help_text = '<div></div>Wymagana. 150 lub mniej znaków. Jedynie litery, cyfry i @/./+/-/_.'
        self.fields['password2'].help_text = ''

    class Meta:
        model = User
        fields = ['username', 'first_name', 'email', 'telefon', 'password1', 'password2']

class UserLoginForm(forms.Form):
    username = forms.CharField(label='', max_length=100, widget=forms.TextInput(attrs = {'class': 'rejestracja_input', 'type': 'text', 'placeholder': 'Login', 'onfocus': "this.placeholder=''", 'onblur': "this.placeholder='Login'"}))
    password = forms.CharField(label='', max_length=100, widget=forms.TextInput(attrs = {'class': 'rejestracja_input', 'type': 'text', 'placeholder': 'Hasło', 'onfocus': "this.placeholder=''", 'onblur': "this.placeholder='Hasło'"}))

    class Meta:
        model = User
        fields = ['username', 'password']

class ChangePassClick(forms.Form):
    password = forms.CharField()

class PasswordChange(PasswordChangeForm):
    def __init__(self, *args, **kwargs):
        super(PasswordChange, self).__init__(*args, **kwargs)
        self.fields['old_password'].widget.attrs = {'class': 'rejestracja_input', 'type': 'text', 'placeholder': 'Stare haslo', 'onfocus': "this.placeholder=''", 'onblur': "this.placeholder='Stare haslo'"}
        self.fields['new_password1'].widget.attrs = {'class': 'rejestracja_input', 'type': 'text', 'placeholder': 'Nowe haslo', 'onfocus': "this.placeholder=''", 'onblur': "this.placeholder='Nowe haslo'"}
        self.fields['new_password2'].widget.attrs = {'class': 'rejestracja_input', 'type': 'text', 'placeholder': 'Powtorz nowe haslo', 'onfocus': "this.placeholder=''", 'onblur': "this.placeholder='Powtorz nowe haslo'"}
        self.fields['old_password'].label = ''
        self.fields['new_password1'].label = ''
        self.fields['new_password2'].label = ''
        self.fields['new_password1'].help_text = '<div><br></div><ul style="list-style:none; padding:0; margin:0;"><li>Twoje hasło nie może być zbyt podobne do twoich innych danych osobistych.</li><li>Twoje hasło musi zawierać co najmniej 8 znaków.</li>\
        <li>Twoje hasło nie może być powszechnie używanym hasłem.</li><li>Twoje hasło nie może składać się tylko z cyfr.</li></ul></br>'

class AuthChangePass(PasswordChangeForm):
    code = forms.CharField(label='', widget=forms.TextInput(attrs={'class': 'rejestracja_input', 'type': 'text', 'placeholder': 'Kod SMS', 'onfocus': "this.placeholder=''", 'onblur': "this.placeholder='Kod SMS'"}))

    def __init__(self, *args, **kwargs):
        super(AuthChangePass, self).__init__(*args, **kwargs)
        self.fields['old_password'].widget.attrs = {'class': 'rejestracja_input', 'type': 'text', 'placeholder': 'Stare haslo', 'onfocus': "this.placeholder=''", 'onblur': "this.placeholder='Stare haslo'"}
        self.fields['new_password1'].widget.attrs = {'class': 'rejestracja_input', 'type': 'text', 'placeholder': 'Nowe haslo', 'onfocus': "this.placeholder=''", 'onblur': "this.placeholder='Nowe haslo'"}
        self.fields['new_password2'].widget.attrs = {'class': 'rejestracja_input', 'type': 'text', 'placeholder': 'Powtorz nowe haslo', 'onfocus': "this.placeholder=''", 'onblur': "this.placeholder='Powtorz nowe haslo'"}
        self.fields['old_password'].label = ''
        self.fields['new_password1'].label = ''
        self.fields['new_password2'].label = ''
        self.fields['new_password1'].help_text = '<div><br></div><ul style="list-style:none; padding:0; margin:0;"><li>Twoje hasło nie może być zbyt podobne do twoich innych danych osobistych.</li><li>Twoje hasło musi zawierać co najmniej 8 znaków.</li>\
        <li>Twoje hasło nie może być powszechnie używanym hasłem.</li><li>Twoje hasło nie może składać się tylko z cyfr.</li></ul></br>'

class NickChangeForm(UserCreationForm):
    def __init__(self, *args, **kwargs):
        super(NickChangeForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs = {'class': 'rejestracja_input', 'placeholder': 'Nickname', 'onfocus': "this.placeholder=''", 'onblur': "this.placeholder='Nickname'"}
        self.fields['username'].label = ''
        self.fields['username'].help_text = '<div></br></div>150 lub mniej znaków. Jedynie litery, cyfry i @/./+/-/_.'
        del self.fields['password1']
        del self.fields['password2']

    class Meta:
        model = User
        fields = ['username']

class NameChangeForm(UserCreationForm):
    def __init__(self, *args, **kwargs):
        super(NameChangeForm, self).__init__(*args, **kwargs)
        self.fields['first_name'].widget.attrs = {'class': 'rejestracja_input', 'placeholder': 'Imię', 'onfocus': "this.placeholder=''", 'onblur': "this.placeholder='Imię'"}
        self.fields['first_name'].label = ''
        del self.fields['password1']
        del self.fields['password2']

    class Meta:
        model = User
        fields = ['first_name']

class EmailChangeForm(UserCreationForm):
    email = forms.EmailField(label='', required=True, widget=forms.EmailInput(attrs = {'class': 'rejestracja_input', 'placeholder': 'Email', 'onfocus': "this.placeholder=''", 'onblur': "this.placeholder='Email'"}))
    def __init__(self, *args, **kwargs):
        super(EmailChangeForm, self).__init__(*args, **kwargs)
        del self.fields['password1']
        del self.fields['password2']
    class Meta:
        model = User
        fields = ['email']

class PhoneChangeForm(UserCreationForm):
    telefon = PhoneNumberField(label='')
    telefon.widget.build_attrs({'class': 'rejestracja_input', 'placeholder': 'Telefon', 'onfocus': "this.placeholder=''", 'onblur': "this.placeholder='Telefon'"})

    def __init__(self, *args, **kwargs):
        super(PhoneChangeForm, self).__init__(*args, **kwargs)
        del self.fields['password1']
        del self.fields['password2']

    class Meta:
        model = User
        fields = ['telefon']




    
