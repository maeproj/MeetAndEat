from django.shortcuts import render
from django.http import HttpResponse
from users.models import NewUser

def home(request):
    return render(request, 'home/home.html')
