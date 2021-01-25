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


def home(request):
    return render(request, 'home/home.html')

def chat(request):
    return render(request, 'home/chat.html')

def kontakt(request):
    return render(request, 'home/kontakt.html')

def restauracja(request):
    return render(request, 'home/restauracja.html')