from django.contrib import admin

from market.models import Category, Order, Product

# Register your models here.
admin.site.register(Order)
admin.site.register(Product)
admin.site.register(Category)