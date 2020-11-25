from django.shortcuts import render, redirect
from django.conf import settings
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from datetime import date, timedelta
from .forms import UserRegisterForm, UserLoginForm
from .models import NewUser


def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.refresh_from_db()
            user.save()
            messages.success(request, f'Twoje konto zostało założone, możesz sie teraz zalogować!')
            return redirect('login')
    else:
        form = UserRegisterForm()
    return render(request, 'users/register.html', {'form': form})

@login_required
def profile(request):
    return render(request, 'users/profile.html')

def login_user(request):
    if request.method == 'POST':
        login_form = UserLoginForm(request.POST)
        if login_form.is_valid():
            username = request.POST['username']
            password = request.POST['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                if user.is_active:
                    if date.today() - user.newuser.password_date > timedelta(days=30):
                        login(request, user)
                        messages.error(request, "Twoje hasło wygasło. Proszę wprowadzić nowe hasło.")
                        return redirect('change_password')
                    else:
                        login(request, user)
                        return redirect('home')
            else:
                messages.error(request, f'Błędny login lub hasło')
                return redirect('login')
    else:
       login_form = UserLoginForm();
    return render(request, 'users/login.html', {'form': login_form})

def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(request, 'Twoje hasło zostało pomyślnie zmienione :)')
            user.newuser.password_date = date.today()
            user.save()
            return redirect('home')
        else:
            messages.error(request, 'Nieprawidłowe dane :(')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'users/change_pass.html', {'form':form})



