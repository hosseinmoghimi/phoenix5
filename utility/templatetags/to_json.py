
from django import template
register = template.Library()
from archive.serializers import FolderSerializer,FileSerializer
import json


from warehouse.serializers import WareHouseSerializer
from accounting.serializers import AccountSerializer,ProfileSerializer, TransactionSerializer


@register.filter
def to_json_warehouses(warehouses):
    return json.dumps(WareHouseSerializer(warehouses,many=True).data)

@register.filter
def to_json_accounts(accounts):
    return json.dumps(AccountSerializer(accounts,many=True).data)

@register.filter
def to_json_profiles(profiles):
    return json.dumps(ProfileSerializer(profiles,many=True).data)
@register.filter
def to_json_transactions(transactions):
    return json.dumps(TransactionSerializer(transactions,many=True).data)


@register.filter
def to_json_folders(folders):
    return json.dumps(FolderSerializer(folders,many=True).data)

@register.filter
def to_json_folder(folder):
    return json.dumps(FolderSerializer(folder).data)

@register.filter
def to_json_files(files):
    return json.dumps(FileSerializer(files,many=True).data)
