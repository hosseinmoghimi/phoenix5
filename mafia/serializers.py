from rest_framework import serializers
from mafia.models import God,Game,Role,Player,RolePlayer


class RoleSerializer(serializers.ModelSerializer):
    class Meta:
        model=Role
        fields=['id','title','get_absolute_url','thumbnail']