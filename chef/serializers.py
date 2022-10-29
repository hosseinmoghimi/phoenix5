from rest_framework import serializers
from chef.models import Food, Guest, Host, Meal, ReservedMeal
from accounting.serializers import AccountSerializer
class FoodSerializer(serializers.ModelSerializer):
    class Meta:
        model = Food
        fields=['id','title','get_absolute_url']

        
class GuestSerializer(serializers.ModelSerializer):
    account=AccountSerializer()
    class Meta:
        model=Guest
        fields=['id','account','get_absolute_url']
class HostSerializer(serializers.ModelSerializer):
    account=AccountSerializer()
    class Meta:
        model=Host
        fields=['id','account','title','get_absolute_url','get_edit_url']
        
class MealSerializer(serializers.ModelSerializer):
    foods=FoodSerializer(many=True)
    host=HostSerializer()
    class Meta:
        model=Meal
        fields=['id','title','foods','host' ,'reserved','reserves_count','max_reserve','persian_date_served','get_edit_url','get_absolute_url','meal_type']

class ReservedMealSerializer(serializers.ModelSerializer):
    meal=MealSerializer()
    guest=GuestSerializer()
    class Meta:
        model=ReservedMeal
        fields=['id','meal','quantity','guest' ,'persian_date_served','persian_date_reserved','get_edit_url','get_absolute_url']
