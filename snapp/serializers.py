from core.serializers import serializers
from accounting.serializers import CategorySerializer,ProductSerializer
from .models import Shipper,Menu,Packer
from market.serializers import SupplierSerializer,ProductOrServiceSerializer,Shop

class ShipperSerializer(serializers.ModelSerializer):
    class Meta:
        model=Shipper
        fields=["id","title"]


class ShopSerializer(serializers.ModelSerializer):
    product_or_service=ProductOrServiceSerializer()
    supplier=SupplierSerializer() 
    class Meta:
        model=Shop
        fields=['id','product_or_service','level','supplier','specifications','unit_price','in_carts','available','unit_name','get_absolute_url','get_edit_url']

        
class MenuSerializer(serializers.ModelSerializer):
    class Meta:
        model=Menu
        fields=["id","title","thumbnail","get_absolute_url"]