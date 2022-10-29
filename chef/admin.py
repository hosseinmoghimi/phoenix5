from django.contrib import admin

from chef.models import Food, Guest, Host, Meal, ReservedMeal
# Register your models here.
admin.site.register(Food) 
admin.site.register(Guest) 
admin.site.register(Meal) 
admin.site.register(ReservedMeal) 
admin.site.register(Host) 