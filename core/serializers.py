from rest_framework import serializers
from .models import Download, Image, Page, PageComment, PageDownload, PageImage, PageLike, PagePermission, PageTag, Parameter,PageLink, Tag
from authentication.serializers import ProfileSerializer


class ParameterSerializer(serializers.ModelSerializer):
    class Meta:
        model=Parameter
        fields=['id','name','value','get_edit_url','get_delete_url']


class PageSerializer(serializers.ModelSerializer):
    class Meta:
        model=Page
        fields=['id','title','get_absolute_url']

class PageDecodeSerializer(serializers.ModelSerializer):
    class Meta:
        model=Page
        fields=['id','short_description','description','get_absolute_url']


class PageFullSerializer(serializers.ModelSerializer):
    class Meta:
        model=Page
        fields=['id','title','class_title','app_name','get_absolute_url','get_delete_url','get_edit_url','get_print_url','get_show_url']


class PagePermissionSerializer(serializers.ModelSerializer):
    profile=ProfileSerializer()
    page=PageSerializer()
    class Meta:
        model=PagePermission
        fields=['id','page','can_write','profile']



class PageLikeSerializer(serializers.ModelSerializer):
    class Meta:
        model=PageLike
        fields=['id','class_title','title','thumbnail','get_absolute_url','get_delete_url']




class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model=Tag
        fields=['id','title','get_absolute_url','get_edit_url','get_delete_url']


class PageTagSerializer(serializers.ModelSerializer):
    class Meta:
        model=PageTag
        fields=['id','tag_title','get_tag_url','get_edit_url','get_delete_url']



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
        fields=['id','title','thumbnail','image','get_edit_url','get_delete_url','get_absolute_url']

class PageImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = PageImage
        fields=['id','title','thumbnail','image','get_edit_url','get_delete_url','get_absolute_url']


class PageLinkSerializer(serializers.ModelSerializer):
    class Meta:
        model=PageLink
        fields=['id','title','url','get_edit_url','get_delete_url','get_icon_tag']



class PageDownloadSerializer(serializers.ModelSerializer):
    class Meta:
        model=PageDownload
        fields=['id','title','get_edit_url','get_delete_url','get_download_url','get_icon_tag']



class DownloadSerializer(serializers.ModelSerializer):
    class Meta:
        model=Download
        fields=['id','title','get_edit_url','get_delete_url','get_download_url']


