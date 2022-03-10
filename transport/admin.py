from django.contrib import admin

from transport.models import Area, Driver,Passenger, ServiceMan

# Register your models here.
admin.site.register(Driver)
admin.site.register(Passenger)
admin.site.register(Area)
admin.site.register(ServiceMan)