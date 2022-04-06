from django.contrib import admin

from market.models import Category, Order, Cart

# Register your models here.
admin.site.register(Order)
admin.site.register(Cart)
admin.site.register(Category)