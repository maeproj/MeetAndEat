from django.shortcuts import render, redirect
from django.conf import settings
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User, models
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import forms
from datetime import date, timedelta, datetime, timezone
from .forms import UserRegisterForm, UserLoginForm
from .models import NewUser


def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            users = form.save()
            users.refresh_from_db()
            users.save()
            newuser = NewUser.objects.create(user=users)
            newuser.save()
            messages.success(request, f'Twoje konto zostało założone, możesz sie teraz zalogować!')
            return redirect('login')
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
    return render(request, 'users/profile.html')



