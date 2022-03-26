
from django import template
register = template.Library()
from archive.serializers import FolderSerializer,FileSerializer
import json


@register.filter
def to_json_folders(folders):
    return json.dumps(FolderSerializer(folders,many=True).data)

@register.filter
def to_json_folder(folder):
    return json.dumps(FolderSerializer(folder).data)

@register.filter
def to_json_files(files):
    return json.dumps(FileSerializer(files,many=True).data)
