from rest_framework import serializers
from market.serializers import Customer,AccountSerializer,AreaSerializer,Supplier
from accounting.serializers import InvoiceBriefSerializer
from .models import Order
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
        fields=['id','title','supplier','invoice','customer','sum','persian_date_ordered','persian_date_ordered_tag','get_edit_url','get_delete_url','get_absolute_url']


        