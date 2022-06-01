from rest_framework import serializers
from market.models import Brand, Category,Product, Supplier
from accounting.serializers import ProductSerializer as ProductSerializer_origin

 
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