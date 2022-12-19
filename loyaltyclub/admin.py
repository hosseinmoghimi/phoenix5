from django.contrib import admin
from .models import Order,Coupon,Coef
# Register your models here.
admin.site.register(Order)
admin.site.register(Coef)
admin.site.register(Coupon)
# admin.site.register(Payment)