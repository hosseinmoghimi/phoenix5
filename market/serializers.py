from rest_framework import serializers
from market.models import Brand, CartLine, Category,Product, Shop, Supplier
from accounting.serializers import ProductOrServiceSerializer, ProductSerializer as ProductSerializer_origin

 
class SupplierSerializer(serializers.ModelSerializer):
    class Meta:
        model=Supplier
        fields=['id','title','thumbnail','get_absolute_url']
 
 
class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model=Category
        fields=['id','title','thumbnail','get_absolute_url']
 
class BrandSerializer(serializers.ModelSerializer):
    class Meta:
        model=Brand
        fields=['id','title','get_absolute_url','logo']
 
class CartLineSerializer(serializers.ModelSerializer):
    product_or_service=ProductOrServiceSerializer()
    class Meta:
        model=CartLine
        fields=['id','product_or_service','get_absolute_url']
class ShopSerializer(serializers.ModelSerializer):
    product_or_service=ProductOrServiceSerializer()
    supplier=SupplierSerializer()
    class Meta:
        model=Shop
        fields=['id','product_or_service','supplier','unit_price','in_carts','available','unit_name','get_absolute_url']
class CategorySerializerForApi(serializers.ModelSerializer):
    class Meta:
        model=Category
        fields=['id','title','thumbnail','get_absolute_url','parent_id','get_products_list_url']





class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model=Product
        fields=['id','title','thumbnail','get_absolute_url']
class ProductSerializerForApi(serializers.ModelSerializer):
    class Meta:
        model=Product
        fields=['id','title','thumbnail','get_absolute_url']