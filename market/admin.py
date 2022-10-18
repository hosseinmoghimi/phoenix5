from django.contrib import admin

from market.models import Brand, CartLine, Customer, Order, Shop, Supplier

# Register your models here.
admin.site.register(Brand)
admin.site.register(Order)
admin.site.register(CartLine)
admin.site.register(Supplier)
admin.site.register(Customer)
admin.site.register(Shop)