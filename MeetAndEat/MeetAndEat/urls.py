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
from reservation import views as reservation_views
from menu import views as menu_view
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static
from reservation import views as rezerwacje_view
from django.contrib.staticfiles.urls import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

urlpatterns = [
    path('admin/', admin.site.urls, name='admin'),
    path('register/', user_views.register, name='register'),
    path('profile/', user_views.profile, name='profile'),
    path('home/', home_views.home, name='home'),
    path('login/', user_views.login_user, name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='users/logout.html'), name='logout'),
    path('pass_change/', user_views.change_password, name='change_password'),
    path('menu/', menu_view.menu_orgs, name='menu'),
    #path('desery/', menu_views.menu_desery, name='menu_desery'),
    #path('makarony/', menu_views.menu_makarony, name='menu_makarony'),
    #path('kanapki/', menu_views.menu_kanapki, name='menu_kanapki'),
    #path('pizze/', menu_views.menu_pizze, name='menu_pizze'),
    path('rezerwacje1', reservation_views.reservation, name='reservation1'),
    path('rezerwacje2', reservation_views.menu_orgs, name='reservation2'),
    path('kontakt/', home_views.kontakt, name='kontakt'),
    path('restauracja/', home_views.restauracja, name='restauracja'),
    path('moje_rezerwacje/', user_views.moje_rezerwacje, name='moje_rezerwacje'),
]

urlpatterns += staticfiles_urlpatterns()
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)