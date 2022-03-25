
from django import template
register = template.Library()
from accounting.serializers import AccountSerializer,ProfileSerializer
import json


@register.filter
def to_json_accounts(accounts):
    return json.dumps(AccountSerializer(accounts,many=True).data)

@register.filter
def to_json_profiles(profiles):
    return json.dumps(ProfileSerializer(profiles,many=True).data)