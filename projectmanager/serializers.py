from rest_framework import serializers
from .models import Event,Employee, Letter, Material, MaterialRequest, PM_Service, Request,Project,OrganizationUnit, RequestSignature, ServiceRequest, letterSent
from authentication.serializers import ProfileSerializer


class ProjectBriefSerializer(serializers.ModelSerializer):
    class Meta:
        model=Project
        fields=['id', 'title', 'get_absolute_url']

class OrganizationUnitSerializer(serializers.ModelSerializer):

    class Meta:
        model=OrganizationUnit
        fields=['id','title','image','logo','full_title','pre_title','get_edit_url','get_absolute_url']


class EventSerializerForChart(serializers.ModelSerializer):
    class Meta:
        model=Event
        fields=['id','title','get_absolute_url','start_datetime2','end_datetime2']

class EventSerializer(serializers.ModelSerializer):
    project_related=ProjectBriefSerializer()
    class Meta:
        model=Event
        fields=['id','project_related','thumbnail','likes_count','title','get_absolute_url','persian_event_datetime','persian_start_datetime','persian_end_datetime','get_edit_url']

class LetterSerializer(serializers.ModelSerializer):
    class Meta:
        model=Letter
        fields=['id','thumbnail','title','get_absolute_url','persian_date_added','get_edit_url']

class LetterSentSerializer(serializers.ModelSerializer):
    letter=LetterSerializer()
    sender=OrganizationUnitSerializer()
    recipient=OrganizationUnitSerializer()
    class Meta:
        model=letterSent
        fields=['id','letter','sender','persian_date_sent','recipient']





 

class EmployeeSerializer(serializers.ModelSerializer):
    profile=ProfileSerializer()
    organization_unit=OrganizationUnitSerializer()
    class Meta:
        model=Employee
        fields=['id','organization_unit','mobile','job_title','get_absolute_url','get_delete_url','get_edit_url','profile','title']


class RequestSignatureSerializer(serializers.ModelSerializer):
    employee=EmployeeSerializer()
    class Meta:
        model = RequestSignature
        fields = ['id','employee', 'get_status_tag','persian_date_added','description','get_delete_url','get_edit_url']

class MaterialSerializer(serializers.ModelSerializer):
    class Meta:
        model = Material
        fields = ['id', 'title', 'get_absolute_url','full_title','buy_price','available','unit_price','unit_name','thumbnail']


class ServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = PM_Service
        fields = ['id', 'title', 'get_absolute_url','full_title','buy_price','unit_price','unit_name','thumbnail']


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
        model=ServiceRequest
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
