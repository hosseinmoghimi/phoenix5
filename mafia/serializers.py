from rest_framework import serializers
from mafia.models import GameAct, GameScenario, God,Game,Role,Player,RolePlayer
from authentication.serializers import ProfileSerializer
from accounting.serializers import AccountSerializer

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
    account=AccountSerializer()
    class Meta:
        model=Player
        fields=['id','account','score','get_absolute_url']

class GodSerializer(serializers.ModelSerializer):
    account=AccountSerializer()
    class Meta:
        model=God
        fields=['id','account','get_absolute_url']

class GameSerializer(serializers.ModelSerializer):
    god=GodSerializer()
    class Meta:
        model=Game
        fields=['id','god','title','scenario','status','get_absolute_url']

class RolePlayerSerializer(serializers.ModelSerializer):
    player=PlayerSerializer()
    game=GameSerializer()
    role=RoleSerializer()
    class Meta:
        model=RolePlayer
        fields=['id','role','game','get_absolute_url','player','get_edit_url']

class GameActSerializer(serializers.ModelSerializer):
    actor=RolePlayerSerializer()
    acted=RolePlayerSerializer()
    class Meta:
        model=GameAct
        fields=['id','actor','acted','score','act','night','get_absolute_url','get_edit_url']