from django.contrib import admin
from .models import Area, Location, PageLocation
admin.site.register(Location)
admin.site.register(PageLocation)
admin.site.register(Area)