from rest_framework import serializers
from mafia.models import GameAct, GameScenario, God,Game,Role,Player,RolePlayer
from authentication.serializers import ProfileSerializer

class RoleSerializer(serializers.ModelSerializer):
    class Meta:
        model=Role
        fields=['id','title','color','side','get_absolute_url','thumbnail']

class GameScenarioSerializer(serializers.ModelSerializer):
    roles=RoleSerializer(many=True)
    class Meta:
        model=GameScenario
        fields=['id','title','roles','get_absolute_url']

class PlayerSerializer(serializers.ModelSerializer):
    profile=ProfileSerializer()
    class Meta:
        model=Player
        fields=['id','profile','score','get_absolute_url']

class GodSerializer(serializers.ModelSerializer):
    profile=ProfileSerializer()
    class Meta:
        model=God
        fields=['id','profile','get_absolute_url']

class GameSerializer(serializers.ModelSerializer):
    god=GodSerializer()
    class Meta:
        model=Game
        fields=['id','god','title','scenario','get_absolute_url']

class RolePlayerSerializer(serializers.ModelSerializer):
    player=PlayerSerializer()
    role=RoleSerializer()
    class Meta:
        model=RolePlayer
        fields=['id','role','get_absolute_url','player','get_edit_url']

class GameActSerializer(serializers.ModelSerializer):
    actor=RolePlayerSerializer()
    acted=RolePlayerSerializer()
    class Meta:
        model=GameAct
        fields=['id','actor','acted','score','act','night','get_absolute_url','get_edit_url']