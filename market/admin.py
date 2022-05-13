from django.contrib import admin

from market.models import Category, Customer, Order, Cart, Shop, Supplier

# Register your models here.
admin.site.register(Order)
admin.site.register(Cart)
admin.site.register(Supplier)
admin.site.register(Shop)
admin.site.register(Category)
admin.site.register(Customer)