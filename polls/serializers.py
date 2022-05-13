from rest_framework import serializers
from authentication.serializers import ProfileSerializer

from polls.models import Vote, Option, Poll

class PollSerializer(serializers.ModelSerializer):
    creator=ProfileSerializer()
    class Meta:
        model = Poll
        fields = ['id','title','creator','get_absolute_url','votes_count','options_count','thumbnail']


class OptionSerializer(serializers.ModelSerializer):
    poll=PollSerializer()
    creator=ProfileSerializer()
    class Meta:
        model = Option
        fields = ['id','title','poll','creator','get_absolute_url','thumbnail','votes_count']
class VoteSerializer(serializers.ModelSerializer):
    option=OptionSerializer()
    class Meta:
        model = Vote
        fields = ['id','profile','option']