from django.shortcuts import render, redirect
from django.conf import settings
from django.core.mail import EmailMessage, EmailMultiAlternatives
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User, models
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash, forms
from django.contrib.auth.forms import PasswordChangeForm
from datetime import date, timedelta, datetime, timezone
from .forms import UserRegisterForm, UserLoginForm, ChangePassClick, PasswordChange, AuthChangePass, NickChangeForm, NameChangeForm, EmailChangeForm, PhoneChangeForm
from .models import NewUser, SMSModel
from .tokens import account_activation_token
from MeetAndEat.settings import EMAIL_HOST_USER, TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN, TWILIO_NUMBER, SMS_BROADCAST_TO_NUMBERS
from django.template.loader import get_template
from django.urls import reverse, resolve
import re
from global_modules.models import AllActions
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.utils.encoding import force_bytes, force_text
import random
import string
from twilio.rest import Client

def register(request):
    if request.method == 'POST' and 'regis' in request.POST:
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            users = form.save(commit=False)
            if re.search('[A-ZĄĆĘŁÓŃŻŹŚ]', form.cleaned_data['password1']) is not None:
                if re.search('[.@#$&^_]', form.cleaned_data['password1']) is not None:
                    if re.search('[0-9]', form.cleaned_data['password1']) is not None:
                        if re.match('^[a-zA-ZĄĆĘŁÓŃŻŹŚ.@#&^_0-9]+$', form.cleaned_data['password1']):
                            users.save()
                            newuser = NewUser.objects.create(user=users, phone=form.cleaned_data['telefon'], password_history = form.cleaned_data['password1'])
                            newuser.save()
                            messages.success(request, 'Twoje konto zostało założone, możesz sie teraz zalogować!')
                            AllActions.objects.create(user=users, action_id=1, action=f"założenie konta")
                            return redirect('home')
                        else:
                            messages.error(request, 'Wpisano nielegalne znaki')
                    else:
                        messages.error(request, 'Brak cyfry w haśle')
                        return redirect('register')
                else:
                    messages.error(request, 'Brak znaku specjalnego w haśle')
                    return redirect('register')
            else:
                messages.error(request, 'Brak wielkiej litery w haśle')
                return redirect('register')

    else:
        form = UserRegisterForm()

    return render(request, 'users/register.html', {'form_reg': form})

def logowanie(request):
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
                            AllActions.objects.create(user=user, action_id=4, action="proba logowania na blokadzie czasowej")
                            return redirect('home')
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
                        AllActions.objects.create(user=user, action_id=5, action="przekroczenie liczby logowań")
                        messages.error(request, 'Przekroczono limit logowań, proszę poczekać 30 minut przed następną próbą')
                        return redirect('login')
                    messages.error(request, f'Nieprawidłowe dane, pozostało prób: {ent}')
                    return redirect('login')
                messages.error(request, f'Błędny login lub hasło')
                return redirect('login')

    else:
       login_form = UserLoginForm();

    return render(request, 'users/logowanie.html', {'form': login_form})

def change_password(request):
    if request.method == 'POST':
        form = PasswordChange(request.user, request.POST)
        if form.is_valid():
            if form.cleaned_data['new_password1'] == form.cleaned_data['old_password']:
                messages.error(request, 'Nieprawidłowe dane :(')
            else:
                user = form.save()
                person = NewUser.objects.get(user=user)
                if re.search('[A-ZĄĆĘŁÓŃŻŹŚ]', form.cleaned_data['password1']) is not None:
                    if re.search('[.@#$&^_]', form.cleaned_data['password1']) is not None:
                        if re.search('[0-9]', form.cleaned_data['password1']) is not None:
                            if form.cleaned_data['old_password'] not in person.password_history:
                                AllActions.objects.create(user=user, action_id=6, action="Błąd przy zmianie hasła: stare hasło nie pasuje")
                                messages.error(request, 'Błędne stare hasło')
                            elif form.cleaned_data['new_password1'] in person.password_history:
                                AllActions.objects.create(user=user, action_id=7, action="Błąd przy zmianie hasła: nowe hasło już było rejestrowane")
                                messages.error(request, 'Hasło było już używane, proszę wpisać nowe hasło')
                            else:
                                user.refresh_from_db()
                                user.save()
                                messages.success(request, 'Twoje hasło zostało pomyślnie zmienione :)')
                                person.password_date = date.today()
                                person.password_history += ',' + form.cleaned_data['new_password1']
                                person.save()
                                update_session_auth_hash(request, user)
                                AllActions.objects.create(user=user, action_id=8, action="pomyślna zmiana hasła")
                                login(request, user)
                                return redirect('home')
                        else:
                            messages.error(request, 'Brak cyfry w haśle')
                            return redirect('register')
                    else:
                        messages.error(request, 'Brak znaku specjalnego w haśle')
                        return redirect('register')
                else:
                    messages.error(request, 'Brak wielkiej litery w haśle')
                    return redirect('register')
        else:
            messages.error(request, 'Nieprawidłowe dane :(')
    else:
        form = PasswordChange(request.user)
    return render(request, 'users/change_pass.html', {'form_ch':form})

@login_required
def profile(request):
    data = {}
    user = User.objects.get(username=request.user.username)
    user_ex = NewUser.objects.get(user=request.user)
    s = list(user_ex.phone.as_e164)
    s.insert(3, ' ')
    s[7:] = '*' * len(s[7:])
    num = ''.join(s)
    data['phone'] = num
    data['username'] = user.username
    data['email'] = user.email
    data['first_name'] = user.first_name

    form = ChangePassClick()
    nick_form = NickChangeForm()
    name_form = NameChangeForm()
    mail_form = EmailChangeForm()
    phone_form = PhoneChangeForm()
    
    if request.method == 'POST':
        if 'pass_change_butt' in request.POST:
            form = ChangePassClick(request.POST)
            if form.is_valid():
                if user.check_password(form.cleaned_data['password']):
                    if user_ex.pass_change_entries > 2:
                        if datetime.now(timezone.utc) - user_ex.pass_timeout < timedelta(days=1):
                            messages.error('Prośba o zmianę hasła zablokowana, blokada zniknie po 24h')
                            AllActions.objects.create(user=user, action_id=24, action="PROFIL: Próba prośby o zmiane hasła przy blokadzie")
                            return redirect('profile')
                        else:
                            AllActions.objects.create(user=user, action_id=25, action="PROFIL: Wyzerowanie użytkownikowi licznika prób zmiany hasła")
                            user_ex.pass_change_entries = 0
                            user_ex.pass_timeout = None
                            user_ex.save()

                    uid = urlsafe_base64_encode(force_bytes(user.pk))
                    token = account_activation_token.make_token(user)
                    subject = 'Zmiana hasła'
                    from_email = EMAIL_HOST_USER
                    plain_text = get_template('email.txt')
                    htmly = get_template('email.html')
                    d = {'username': user, 'url': reverse('auth_pass_change', kwargs={'uidb64': str(uid), 'token': token})}
                    text_content = plain_text.render(d)
                    html_content = htmly.render(d)
                    msg = EmailMultiAlternatives(subject, text_content, from_email, ['ooracuchoo@gmail.com'])
                    msg.attach_alternative(html_content, 'text/html')
                    msg.send()
                    AllActions.objects.create(user=user, action_id=23, action="PROFIL: Wniesienie o zmianę hasła")
                    try:
                        sms_model_delete = SMSModel.objects.get(user=request.user, to_delete=True)
                        sms_model_delete.delete()
                    except:
                        pass

                    return redirect('profile')
                else:
                    messages.error(request, 'Podano złe hasło')

        elif 'nick_change_butt' in request.POST:
            nick_form = NickChangeForm(request.POST)
            if nick_form.is_valid():
                request.user.username = nick_form.cleaned_data['username']
                request.user.save()
                return redirect('profile')

        elif 'name_change_butt' in request.POST:
            name_form = NameChangeForm(request.POST)
            if name_form.is_valid():
                request.user.first_name = name_form.cleaned_data['first_name']
                request.user.save()
                return redirect('profile')

        elif 'mail_change_butt' in request.POST:
            mail_form = EmailChangeForm(request.POST)
            if mail_form.is_valid():
                request.user.email = mail_form.cleaned_data['email']
                request.user.save()
                return redirect('profile')

        elif 'phone_change_butt' in request.POST:
            phone_form = PhoneChangeForm(request.POST)
            if phone_form.is_valid():
                try:
                    person = NewUser.objects.get(user=request.user)
                    person.phone = phone_form.cleaned_data['telefon']
                    person.save()
                except:
                    messages.warning(request, 'Podany numer jest już zarejestrowany')
                return redirect('profile')

    return render(request, 'users/profile.html', {'data': data, 'nick_form': nick_form, 'name_form': name_form, 'mail_form': mail_form, 'phone_form': phone_form, 'form_prof': form})

def moje_rezerwacje(request):
    pass

@login_required
def auth_change_password(request, uidb64, token):
    sms_model_delete = None
    try:
        sms_model_delete = SMSModel.objects.get(user=request.user, to_delete=True)
    except:
        pass
    if sms_model_delete is not None:
        AllActions.objects.create(user=request.user, action_id=19, action="AUTH: Próba zmiany hasła mimo braku zezwolenia")
        messages.error(request, f'Kod weryfikacyjny stracił ważność: zbyt duża ilość prób')
        return redirect('home')

    person = NewUser.objects.get(user=request.user)
    sms_model = None
    try:
        sms_model = SMSModel.objects.get(user=request.user, to_delete=False)
    except:
        pass

    if sms_model == None:
        code = ''.join(random.choice(string.ascii_letters + string.digits) for i in range(6))
        message_to_broadcast = ('Kod weryfikacyjny: ' + code)

        client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
        client.messages.create(to='+48784950705', from_=TWILIO_NUMBER, body=message_to_broadcast)

        sms_model = SMSModel.objects.create(user=request.user, code=code)
        sms_model.save()
        AllActions.objects.create(user=request.user, action_id=20, action=f"AUTH: Wysłanie wiadomości z kodem weryfikacyjnym do {{request.user.username}}")
        
    if request.method == 'POST' and 'change_imp' in request.POST:
        try:
            uid = force_text(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist) as e:
            messages.warning(request, str(e))
            user = None
        if user is not None and account_activation_token.check_token(user, token):
            form = AuthChangePass(request.user, request.POST)
            if form.is_valid():
                if form.cleaned_data['code'] != sms_model.code:
                    sms_model.failed_attempts += 1
                    sms_model.save()
                    if sms_model.failed_attempts > 2:
                        sms_model.failed_attempts = 0
                        sms_model.save()
                        person.pass_change_entries += 1
                        if person.pass_change_entries > 2:
                            person.pass_timeout = datetime.now()
                            person.save()
                            messages.error(request, 'Zablokowano możliwość generowania kodów. Blokada zniknie po 24h.')
                            return redirect('home')
                        messages.error(request, f'Kod weryfikacyjny stracił ważność: zbyt duża ilość prób')
                        person.save()
                        AllActions.objects.create(user=user, action_id=22, action="AUTH: Utrata ważności kodu - zbyt duża ilość prób")
                        sms_model.to_delete = True
                        sms_model.save()
                        return redirect('home')
                    messages.error(request, 'Błędny kod weryfikacyjny')
                    AllActions.objects.create(user=user, action_id=21, action="AUTH: Błędny kod weryfikacyjny")
                    return redirect('auth_pass_change', uidb64 = uidb64, token=token)

                if form.cleaned_data['new_password1'] == form.cleaned_data['old_password']:
                    messages.error(request, 'Nieprawidłowe dane :(')
                else:
                    user = form.save()
                    person = NewUser.objects.get(user=user)
                    if re.search('[A-ZĄĆĘŁÓŃŻŹŚ]', form.cleaned_data['new_password1']) is not None:
                        if re.search('[.@#$&^_]', form.cleaned_data['new_password1']) is not None:
                            if re.search('[0-9]', form.cleaned_data['new_password1']) is not None:
                                if form.cleaned_data['old_password'] not in person.password_history:
                                    AllActions.objects.create(user=user, action_id=17, action="AUTH: Błąd przy zmianie hasła: stare hasło nie pasuje")
                                    messages.error(request, 'Błędne stare hasło')
                                elif form.cleaned_data['new_password1'] in person.password_history:
                                    AllActions.objects.create(user=user, action_id=18, action="AUTH: Błąd przy zmianie hasła: nowe hasło już było rejestrowane")
                                    messages.error(request, 'Hasło było już używane, proszę wpisać nowe hasło')
                                else:
                                    user.refresh_from_db()
                                    user.save()
                                    messages.success(request, 'Twoje hasło zostało pomyślnie zmienione :)')
                                    person.password_date = date.today()
                                    person.password_history += ',' + form.cleaned_data['new_password1']
                                    person.save()
                                    update_session_auth_hash(request, user)
                                    AllActions.objects.create(user=user, action_id=8, action="pomyślna zmiana hasła")
                                    sms_model.delete()
                                    return redirect('home')
                            else:
                                messages.error(request, 'Brak cyfry w haśle')
                                return redirect('auth_pass_change', uidb64 = uidb64, token=token)
                        else:
                            messages.error(request, 'Brak znaku specjalnego w haśle')
                            return redirect('auth_pass_change', uidb64 = uidb64, token=token)
                    else:
                        messages.error(request, 'Brak wielkiej litery w haśle')
                        return redirect('auth_pass_change', uidb64 = uidb64, token=token)
            else:
                messages.error(request, 'Nie udało się zmienić hasła')
                return render(request, 'users/auth_change_pass.html', {'form_auth': form, 'uidb64': uidb64, 'token': token})
    else:
        try:
            uid = force_text(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist) as e:
            messages.warning(request, str(e))
            user = None
        if user is not None and account_activation_token.check_token(user, token):
            form = AuthChangePass(request.user)
            return render(request, 'users/auth_change_pass.html', {'form_auth': form, 'uidb64': uidb64, 'token': token})


