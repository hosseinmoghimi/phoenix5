from core.serializers import serializers
from accounting.serializers import CategorySerializer,ProductSerializer
from .models import Shipper
class ShipperSerializer(serializers.ModelSerializer):
    class Meta:
        model=Shipper
        fields=["id","title"]