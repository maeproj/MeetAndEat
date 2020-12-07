from django.shortcuts import render, redirect
from .forms import ReservationForm
from datetime import date, time
from django.contrib import messages

def reservation(request):
    if request.method == 'POST':
        form = ReservationForm(request.POST)
        if form.is_valid():
            day = form.cleaned_data['day']
            begin_h = form.cleaned_data['begin_h']
            begin_m = form.cleaned_data['begin_m']
            end_h = form.cleaned_date['end_h']
            end_m = form.cleaned_date['end_m']

            if day < date.today():
                messages.error(request, 'Nie można zarezerwować stolika na datę przeszłą')
                return redirect('reservation')
            
    else:
        form = ReservationForm()
    return render(request, 'reservation/rezerwacje.html', {'form':form})
