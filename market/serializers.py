from rest_framework import serializers
from market.models import Category,Product
from accounting.serializers import ProductSerializer as ProductSerializer_origin

 
 
class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model=Category
        fields=['id','title','thumbnail','get_absolute_url']
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