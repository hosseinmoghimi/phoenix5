from django.contrib import admin

from market.models import Brand, CartLine, Customer, Order, Cart, Shop, Supplier

# Register your models here.
admin.site.register(Brand)
admin.site.register(Order)
admin.site.register(Cart)
admin.site.register(Supplier)
admin.site.register(Customer)
admin.site.register(Shop)
admin.site.register(CartLine)