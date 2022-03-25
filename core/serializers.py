from rest_framework import serializers
from .models import Image, Page, PageComment, PageDownload, PageImage, PageLike, Parameter,PageLink
from authentication.serializers import ProfileSerializer


class ParameterSerializer(serializers.ModelSerializer):
    class Meta:
        model=Parameter
        fields=['id','name','value','get_edit_url','get_delete_url']



class PageLikeSerializer(serializers.ModelSerializer):
    class Meta:
        model=PageLike
        fields=['id','class_title','title','thumbnail','get_absolute_url','get_delete_url']




class PageBriefSerializer(serializers.ModelSerializer):
    class Meta:
        model=Page
        fields=['id','class_title','title','thumbnail','get_absolute_url','get_delete_url']


class PageCommentSerializer(serializers.ModelSerializer):
    profile=ProfileSerializer()
    class Meta:
        model = PageComment
        fields=['id','comment','persian_date_added','profile']
        
class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields=['id','title','thumbnail','image','get_edit_url','get_delete_url']

class PageImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = PageImage
        fields=['id','title','thumbnail','image','get_edit_url','get_delete_url']


class PageLinkSerializer(serializers.ModelSerializer):
    class Meta:
        model=PageLink
        fields=['id','title','url','get_edit_url','get_delete_url']



class PageDownloadSerializer(serializers.ModelSerializer):
    class Meta:
        model=PageDownload
        fields=['id','title','get_edit_url','get_delete_url','get_download_url']


