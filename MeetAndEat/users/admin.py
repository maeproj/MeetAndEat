from django.contrib import admin
from .models import NewUser, SMSModel

# Register your models here.
class HomeAdmin(admin.ModelAdmin):
    list_display = ('user', 'password_date')

admin.site.register(NewUser, HomeAdmin)
admin.site.register(SMSModel)