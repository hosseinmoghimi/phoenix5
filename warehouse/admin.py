from django.contrib import admin

# Register your models here.

from warehouse.models import WareHouse,WareHouseSheet
# Register your models here.
admin.site.register(WareHouse)
admin.site.register(WareHouseSheet)