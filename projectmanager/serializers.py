from rest_framework import serializers
from .models import Employee, Material, Request,Service,Project,OrganizationUnit
from authentication.serializers import ProfileSerializer


class EmployeeSerializer(serializers.ModelSerializer):
    profile=ProfileSerializer()
    class Meta:
        model=Employee
        fields=['id','get_absolute_url','profile']



class OrganizationUnitSerializer(serializers.ModelSerializer):

    class Meta:
        model=OrganizationUnit
        fields=['id','title','image','full_title','pre_title','get_edit_url','get_absolute_url']


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
 


class ServiceRequestSerializer(serializers.ModelSerializer):
    service=ServiceSerializer()
    project=ProjectSerializer()
    employee=EmployeeSerializer()
    class Meta:
        model=Request
        fields=['id','total','service','persian_date_requested',
        'quantity','persian_date_added','get_edit_url','get_delete_url',
        'get_status_tag','project','employee','unit_name','unit_price',
        'get_absolute_url']

class MaterialRequestSerializer(serializers.ModelSerializer):
    material=MaterialSerializer()
    project=ProjectSerializer()
    employee=EmployeeSerializer()
    class Meta:
        model=Request
        fields=['id','total','material','persian_date_requested',
        'quantity','persian_date_added','get_edit_url','get_delete_url',
        'get_status_tag','project','employee','unit_name','unit_price',
        'get_absolute_url']
