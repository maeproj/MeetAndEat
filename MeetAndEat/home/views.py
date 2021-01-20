from django.shortcuts import render, redirect
from django.http import HttpResponse
from users.models import NewUser
from users.forms import UserLoginForm
from django.contrib import messages
from global_modules.models import AllActions
from datetime import date, datetime, timedelta, time, timezone
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash, forms
from django.urls import resolve
from django.contrib.auth.models import User

def login_template(request):
    if request.method == 'POST' and 'logowanie' in request.POST:
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
                            AllActions.objects.create(user=user, action_id=4, action="proba logowania na blokadzie czasowej")
                            return redirect(resolve(request.path_info).url_name)
                        else:
                            person.entries = 0
                            person.timeout = None
                            person.save()
                    if date.today() - person.password_date > timedelta(days=30):
                        person.entries = 0
                        person.timeout = None
                        person.save()
                        login(request, user)
                        messages.error(request, "Twoje hasło wygasło. Proszę wprowadzić nowe hasło.")
                        AllActions.objects.create(user=user, action_id=3, action="logowanie prowadzące do zmiany hasła")
                        return redirect('change_password')
                    else:
                        login(request, user)
                        AllActions.objects.create(user=user, action_id=2, action="logowanie")
                        messages.success(request, 'Zalogowano pomyślnie')
                        return redirect(resolve(request.path_info).url_name)
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
                        AllActions.objects.create(user=user, action_id=5, action="przekroczenie liczby logowań")
                        messages.error(request, 'Przekroczono limit logowań, proszę poczekać 30 minut przed następną próbą')
                        return redirect(resolve(request.path_info).url_name)
                    messages.error(request, f'Nieprawidłowe dane, pozostało prób: {ent}')
                    return redirect(resolve(request.path_info).url_name)
                messages.error(request, f'Błędny login lub hasło')
                return redirect(resolve(request.path_info).url_name)

    else:
       login_form = UserLoginForm();

    return login_form


def home(request):
    login_form = login_template(request)
    if type(login_form) == type(UserLoginForm()):
        return render(request, 'home/home.html', {'form': login_form})
    else:
        return render(request, 'home/home.html', {'form': UserLoginForm()})

def kontakt(request):
    return render(request, 'home/kontakt.html')

def restauracja(request):
    return render(request, 'home/restauracja.html')