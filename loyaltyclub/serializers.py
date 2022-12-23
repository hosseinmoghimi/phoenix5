from rest_framework import serializers
from market.serializers import Customer,AccountSerializer,AreaSerializer,Supplier
from accounting.serializers import InvoiceBriefSerializer
from .models import Order,Coupon,Coef,DiscountPay
class CustomerSerializer(serializers.ModelSerializer):
    account=AccountSerializer()
    region=AreaSerializer()
    class Meta:
        model=Customer
        fields=['id','region','account','get_absolute_url','get_loyaltyclub_absolute_url']

        
class SupplierSerializer(serializers.ModelSerializer):
    account=AccountSerializer()
    region=AreaSerializer()
    class Meta:
        model=Supplier
        fields=['id','region','account','get_absolute_url','get_loyaltyclub_absolute_url']

        
class OrderSerializer(serializers.ModelSerializer):
    supplier=SupplierSerializer()
    customer=CustomerSerializer()
    invoice=InvoiceBriefSerializer()
    class Meta:
        model=Order
        fields=['id','title','paid','supplier','ship_fee','paid','invoice','customer','discount','sum','persian_date_ordered','persian_date_ordered_tag','get_edit_url','get_delete_url','get_absolute_url']

 
class CoefSerializer(serializers.ModelSerializer):
    class Meta:
        model=Coef
        fields=['id','number','percentage','tartib']

 
# class PaymentSerializer(serializers.ModelSerializer):
#     customer=CustomerSerializer()
#     class Meta:
#         model=Payment
#         fields=['id','customer','coupon_amount','cash_amount','get_edit_url','get_delete_url','get_absolute_url']

 
       
        
class CouponSerializer(serializers.ModelSerializer):
    order=OrderSerializer()
    class Meta:
        model=Coupon
        fields=['id','order','title','amount','get_edit_url','get_delete_url','get_absolute_url']

 
        
class DiscountPaySerializer(serializers.ModelSerializer):
    order=OrderSerializer()
    class Meta:
        model=DiscountPay
        fields=['id','order','title','amount','get_edit_url','get_delete_url','get_absolute_url']
