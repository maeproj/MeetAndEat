from django.contrib import admin
from .models import Menu_item, Menu_org, Reservation, Skladnik, Stolik_item

# Register your models here.
admin.site.register(Menu_item)
admin.site.register(Menu_org)
admin.site.register(Reservation)
admin.site.register(Skladnik)
admin.site.register(Stolik_item)

