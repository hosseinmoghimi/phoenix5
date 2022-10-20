from django.contrib import admin

from market.models import Brand, CartLine, Customer, MarketInvoice, Order, Shop, Supplier

# Register your models here.
admin.site.register(Brand)
admin.site.register(CartLine)
admin.site.register(Customer)
admin.site.register(MarketInvoice)
admin.site.register(Order)
admin.site.register(Shop)
admin.site.register(Supplier)