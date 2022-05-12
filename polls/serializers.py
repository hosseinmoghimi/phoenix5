from rest_framework import serializers

from polls.models import Option, Poll

class PollSerializer(serializers.ModelSerializer):
    class Meta:
        model = Poll
        fields = ['id','title','creator','get_absolute_url','thumbnail']


class OptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Option
        fields = ['id','title','creator','get_absolute_url','thumbnail']