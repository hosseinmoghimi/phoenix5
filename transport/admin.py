from django.contrib import admin
from transport.enums import WorkEventEnum

from transport.models import Area, Driver, Maintenance,Passenger, ServiceMan, Trip, TripCategory, TripPath, VehicleEvent, VehicleWorkEvent, WorkShift

# Register your models here.
admin.site.register(Driver)
admin.site.register(Passenger)
admin.site.register(Area)
admin.site.register(ServiceMan)
admin.site.register(TripCategory)
admin.site.register(WorkShift)
admin.site.register(VehicleWorkEvent)
admin.site.register(VehicleEvent)
admin.site.register(Maintenance)
admin.site.register(TripPath)
admin.site.register(Trip)