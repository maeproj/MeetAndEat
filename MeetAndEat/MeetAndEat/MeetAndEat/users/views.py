from django.shortcuts import render, redirect
from django.conf import settings
from django.core.mail import EmailMessage, EmailMultiAlternatives
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User, models
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import forms
from datetime import date, timedelta, datetime, timezone
from .forms import UserRegisterForm, UserLoginForm, ChangePassClick
from .models import NewUser
from django.template.loader import get_template
#from django.urls import reverse
import re


def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            users = form.save()
            users.refresh_from_db()
            users.save()
            if len(form.cleaned_data['password1']) > 8:
                if re.search('[A-ZĄĆĘŁŃÓŚŻŹ]', form.cleaned_data['password1']) is not None:
                    if re.search('[.@#$&!]', form.cleaned_data['password1']) is not None:
                        if re.search('[0-9]', form.cleaned_data['password1']) is not None:
                            newuser = NewUser.objects.create(user=users)
                            newuser.phone = form.cleaned_data['telefon']
                            newuser.save()
                            messages.success(request, 'Twoje konto zostało założone, możesz sie teraz zalogować!')
                            return redirect('login')
                        else:
                            messages.error(request, 'Brak cyfry w haśle')
                            return redirect('register')
                    else:
                        messages.error(request, 'Brak znaku specjalnego w haśle')
                        return redirect('register')
                else:
                    messages.error(request, 'Brak dużej litery w haśle')
                    return redirect('register')
            else:
                messages.error(request, 'Za mała liczba znaków w haśle')
                return redirect('register')

    else:
        form = UserRegisterForm()
    return render(request, 'users/register.html', {'form': form})

def login_user(request):
    if request.method == 'POST':
        login_form = UserLoginForm(request.POST)
        if login_form.is_valid():
            username = request.POST['username']
            password = request.POST['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                if user.is_active:
                    person = NewUser.objects.get(user=user)
                    if person.entries >= 5:
                        if datetime.now(timezone.utc) - person.timeout < timedelta(minutes=30):
                            left = 30 - (datetime.now().minute - person.timeout.minute)
                            messages.error(request, f'Przekroczono liczbe logowań, pozostały czas: {left} minut')
                            return redirect('login')
                        else:
                            person.entries = 0
                            person.timeout = None
                            person.save()
                    if date.today() - person.password_date > timedelta(days=30):
                        login(request, user)
                        messages.error(request, "Twoje hasło wygasło. Proszę wprowadzić nowe hasło.")
                        return redirect('change_password')
                    else:
                        login(request, user)
                        return redirect('home')
            else:
                if User.objects.filter(username=username).exists():
                    user = User.objects.get(username=username)
                    person = NewUser.objects.get(user=user)
                    person.entries += 1;
                    person.save()
                    ent = 5 - person.entries
                    if(person.entries >= 5):
                        person.timeout = datetime.now(timezone.utc)
                        person.save()
                        messages.error(request, 'Przekroczono limit logowań, proszę poczekać 30 minut przed następną próbą')
                        return redirect('login')
                    messages.error(request, f'Nieprawidłowe dane, pozostało prób: {ent}')
                    return redirect('login')
                messages.error(request, f'Błędny login lub hasło')
                return redirect('login')

    else:
       login_form = UserLoginForm();
    return render(request, 'users/login.html', {'form': login_form})

@login_required
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            if form.cleaned_data['new_password1'] == form.cleaned_data['old_password']:
                messages.error(request, 'Nieprawidłowe dane :(')
            else:
                user = form.save()
                user.refresh_from_db()
                user.save()
                messages.success(request, 'Twoje hasło zostało pomyślnie zmienione :)')
                person = NewUser.objects.get(user=user)
                person.password_date = date.today()
                person.save()
                update_session_auth_hash(request, user)
                login(request, user)
                return redirect('home')
        else:
            messages.error(request, 'Nieprawidłowe dane :(')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'users/change_pass.html', {'form':form})

@login_required
def profile(request):
    data = {}
    user = request.user
    user_ex = NewUser.objects.get(user=request.user)
    s = list(user_ex.phone.as_e164)
    s[-6:-1] = '*'
    data['phone'] = s
    data['username'] = user.username
    data['email'] = user.email
    data['first_name'] = user.first_name
    
    if request.method == 'POST':
        form = ChangePassClick(request.POST)
        if form.is_valid():
            subject = 'Zmiana hasła'
            from_email = EMAIL_HOST_USER
            plain_text = get_template('email.txt')
            htmly = get_template('email.html')
            d = {'username': user, 'url': reverse('change_password')}
            text_content = plain_text.render(d)
            html_content = htmly.render(d)
            msg = EmailMultiAlternatives(subject, text_content, from_email, [user.email])
            msg.attach_alternative(html_content, 'text/html')
            msg.send()

    else:
        form = ChangePassClick()
    return render(request, 'users/profile.html', {'data': data, 'form': form})



