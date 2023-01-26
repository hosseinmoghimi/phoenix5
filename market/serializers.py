from rest_framework import serializers
from market.models import Brand, CartLine, Category, Customer,Product, Shop, Supplier
from accounting.serializers import AccountSerializer, ProductOrServiceSerializer, ProductSerializer as ProductSerializer_origin,ProductSpecificationSerializer
from map.serializers import AreaSerializer
 
class SupplierSerializer(serializers.ModelSerializer):
    account=AccountSerializer()
    region=AreaSerializer()
    class Meta:
        model=Supplier
        fields=['id','account','title','region','thumbnail','region','get_absolute_url','get_loyaltyclub_absolute_url']
   
 


class CategorySerializerForApi(serializers.ModelSerializer):
    class Meta:
        model=Category
        fields=['id','title','thumbnail','get_absolute_url','parent_id','get_products_list_url']
        

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model=Category
        fields=['id','title','thumbnail','get_absolute_url','get_market_absolute_url']


class BrandSerializer(serializers.ModelSerializer):
    class Meta:
        model=Brand
        fields=['id','title','thumbnail','get_absolute_url']


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model=Product
        fields=['id','title','thumbnail','get_market_absolute_url']

        
class CustomerSerializer(serializers.ModelSerializer):
    account=AccountSerializer()
    region=AreaSerializer()
    class Meta:
        model=Customer
        fields=['id','region','account','get_absolute_url','get_loyaltyclub_absolute_url']
        


class ProductSerializerForApi(serializers.ModelSerializer):
    class Meta:
        model=Product
        fields=['id','title','thumbnail','get_absolute_url']
        
class ShopSerializer(serializers.ModelSerializer):
    product=ProductSerializer()
    supplier=SupplierSerializer()
    specifications=ProductSpecificationSerializer(many=True)
    class Meta:
        model=Shop
        fields=['id','product','level','supplier','specifications','unit_price','in_carts','available','unit_name','get_absolute_url','get_edit_url']

class CartLineSerializer(serializers.ModelSerializer):
    shop=ShopSerializer()
    class Meta:
        model=CartLine
        fields=['id','shop','quantity']
