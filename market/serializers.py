from rest_framework import serializers
from market.models import Category
from accounting.serializers import ProductSerializer as ProductSerializer_origin

class ProductSerializer(ProductSerializer_origin):
    pass
class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model=Category
        fields=['id','title','get_absolute_url']