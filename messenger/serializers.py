from authentication.serializers import ProfileSerializer
from messenger.models import Channel, Member, Message
from rest_framework import serializers
from authentication.models import Profile

class SenderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields=['id','name','image','get_absolute_url']
        
class MessageSerializer(serializers.ModelSerializer):
    sender=SenderSerializer()
    class Meta:
        model = Message
        fields=['id','title','body','sender','perisan_date_send']
        
class ChannelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Channel
        fields=['id','name','key','cluster']
class MemberSerializer(serializers.ModelSerializer):
    channel=ChannelSerializer()
    profile=ProfileSerializer()
    class Meta:
        model = Member
        fields=['id','event','profile','channel']
class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields=['id','title','body','get_absolute_url']