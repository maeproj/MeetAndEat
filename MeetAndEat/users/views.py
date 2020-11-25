from django.shortcuts import render, redirect
from django.conf import settings
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from datetime import date, timedelta
from .forms import UserRegisterForm, UserLoginForm
from .models import NewUser


def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            user = User.objects.filter(username=username)
            newuser = NewUser(user=user)
            newuser.save()
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
            newuser = NewUser.objects.filter(user=user)
            if user is not None:
                if user.is_active:
                    if date.today() - newuser.password_date > timedelta(days=30):
                        return redirect('password_change')
                    else:
                        login(request, user)
                        return redirect('home')
            else:
                messages.error(request, f'Błędny login lub hasło')
                return redirect('login')
    else:
       login_form = UserLoginForm();
    return render(request, 'users/login.html', {'form': login_form})



