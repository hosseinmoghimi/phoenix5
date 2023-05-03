from django.contrib import admin
from .models import Shipper,Menu,Packer

admin.site.register(Packer)
admin.site.register(Shipper)
admin.site.register(Menu)