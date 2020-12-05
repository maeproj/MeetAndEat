from django.shortcuts import render
from .forms import ReservationForm

def reservation(request):
    if request.method == 'POST':
        form = ReservationForm(request.POST)
        if form.is_valid():
            pass
    else:
        form = ReservationForm()
    return render(request, 'reservation/rezerwacje.html', {'form':form})
