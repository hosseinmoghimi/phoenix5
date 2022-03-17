from rest_framework import serializers
from .models import Material,Service,Project,OrganizationUnit




class OrganizationUnitSerializer(serializers.ModelSerializer):

    class Meta:
        model=OrganizationUnit
        fields=['id','title','image','pre_title','get_edit_url','get_absolute_url']


class MaterialSerializer(serializers.ModelSerializer):
    class Meta:
        model = Material
        fields = ['id', 'title', 'get_absolute_url','buy_price','available','unit_price','unit_name','thumbnail']


class ServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Service
        fields = ['id', 'title', 'get_absolute_url','buy_price','unit_price','unit_name','thumbnail']




class ProjectSerializer(serializers.ModelSerializer):
    employer=OrganizationUnitSerializer()
    contractor=OrganizationUnitSerializer()
    class Meta:
        model=Project 
        fields=['id','archive','weight','title','likes_count',
        'get_status_color','employer','contractor',
        'full_title','status','sum_total','get_absolute_url',
        'get_edit_url','short_description','thumbnail','persian_start_date',
        'persian_end_date','percentage_completed']