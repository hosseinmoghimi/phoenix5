from rest_framework import serializers
from chef.models import Food

class FoodSerializer(serializers.ModelSerializer):
    class Meta:
        model = Food
        fields=['id','title','get_absolute_url']