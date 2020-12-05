"""MeetAndEat URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from home import views as home_views
from users import views as user_views
from menu import views as menu_views
from reservation import views as reservation_views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('admin/', admin.site.urls, name='admin'),
    path('register/', user_views.register, name='register'),
    path('profile/', user_views.profile, name='profile'),
    path('home/', home_views.home, name='home'),
    path('login/', user_views.login_user, name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='users/logout.html'), name='logout'),
    path('pass_change/', user_views.change_password, name='change_password'),
    path('reservation/', reservation_views.reservation, name='reservation'),
    path('napoje/', menu_views.menu_napoje, name='menu_napoje'),
    path('desery/', menu_views.menu_desery, name='menu_desery'),
    path('kanapki/', menu_views.menu_kanapki, name='menu_kanapki'),
    path('makarony/', menu_views.menu_makarony, name='menu_makarony'),
    path('pizze/', menu_views.menu_pizze, name='menu_pizze'),
    path('kontakt/', home_views.kontakt, name='kontakt'),
    path('restauracja/', home_views.restauracja, name='restauracja'),
]
