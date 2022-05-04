from rest_framework import serializers
from mafia.models import God,Game,Role,Player,RolePlayer
from authentication.serializers import ProfileSerializer

class RoleSerializer(serializers.ModelSerializer):
    class Meta:
        model=Role
        fields=['id','title','get_absolute_url','thumbnail']

class PlayerSerializer(serializers.ModelSerializer):
    profile=ProfileSerializer()
    class Meta:
        model=Role
        fields=['id','profile','get_absolute_url']

class RolePlayerSerializer(serializers.ModelSerializer):
    player=PlayerSerializer()
    role=RoleSerializer()
    class Meta:
        model=RolePlayer
        fields=['id','role','get_absolute_url','player']