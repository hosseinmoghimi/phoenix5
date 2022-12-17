from rest_framework import serializers
from market.serializers import Customer,AccountSerializer,AreaSerializer
from .models import Order
class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model=Order
        fields=['id','title','sum','persian_date_ordered']


class CustomerSerializer(serializers.ModelSerializer):
    account=AccountSerializer()
    region=AreaSerializer()
    class Meta:
        model=Customer
        fields=['id','region','account','get_absolute_url','get_loyaltyclub_absolute_url']
        