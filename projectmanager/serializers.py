from rest_framework import serializers
from accounting.models import ProductOrService

from accounting.serializers import AccountSerializer, InvoiceSerializer, ProductOrServiceSerializer
from .models import RemoteClient,Service,Material,Event,Employee, MaterialRequest, Request,Project,OrganizationUnit, RequestSignature, ServiceRequest
from authentication.serializers import ProfileSerializer
from organization.serializers import OrganizationUnitSerializer,EmployeeSerializer

class ProjectBriefSerializer(serializers.ModelSerializer):
    class Meta:
        model=Project
        fields=['id', 'title', 'get_absolute_url']



class RemoteClientSerializer(serializers.ModelSerializer):
    class Meta:
        model=RemoteClient
        fields=['id', 'name', 'get_absolute_url', 'get_edit_url','remote_ip','any_desk_address'
                ,'any_desk_password','username','password','identity','ssid','preshared_key'
                ,'frequency','protocol','channel_width','adsl_username','adsl_password',
                'telephone','contact'] 
        
class ProjectSerializerForGuantt(serializers.ModelSerializer):
    class Meta:
        model=Project
        fields=['id','title','get_status_color','color','start_date','end_date','status','sum_total','get_absolute_url','short_description','thumbnail','percentage_completed']



class EventSerializerForChart(serializers.ModelSerializer):
    class Meta:
        model=Event
        fields=['id','title','get_absolute_url','start_datetime2','end_datetime2']


class EventSerializer(serializers.ModelSerializer):
    project_related=ProjectBriefSerializer()
    class Meta:
        model=Event
        fields=['id','project_related','get_delete_url','thumbnail','likes_count','title','get_absolute_url','persian_event_datetime','persian_start_datetime','persian_end_datetime','get_edit_url']


class RequestSignatureSerializer(serializers.ModelSerializer):
    employee=EmployeeSerializer()
    class Meta:
        model = RequestSignature
        fields = ['id','employee', 'get_status_tag','persian_date_added','description','get_delete_url','get_edit_url']


class RequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = Request
        fields = ['id','title','get_status_tag', 'get_absolute_url']


class RequestSignatureForEmployeeSerializer(serializers.ModelSerializer):
    employee=EmployeeSerializer()
    request=RequestSerializer()
    class Meta:
        model = RequestSignature
        fields = ['id','request','employee', 'get_status_tag','persian_date_added','description','get_delete_url','get_edit_url']


class MaterialSerializer(serializers.ModelSerializer):
    class Meta:
        model = Material
        fields = ['id', 'title','get_pm_absolute_url','full_title','buy_price','available','unit_price','unit_name','thumbnail']


class ServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Service
        fields = ['id', 'title','get_pm_absolute_url','get_absolute_url','full_title','buy_price','unit_price','unit_name','thumbnail','get_edit_url','get_delete_url']


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
    invoice=InvoiceSerializer()
    class Meta:
        model=ServiceRequest
        fields=['id','total','invoice','service','persian_date_requested',
        'quantity','persian_date_added','get_edit_url','get_delete_url',
        'get_status_tag','project','employee','unit_name','unit_price','status','row',
        'get_absolute_url']


class ServiceRequestFullSerializer(serializers.ModelSerializer):
    service=ServiceSerializer()
    invoice=InvoiceSerializer()
    project=ProjectSerializer()
    employee=EmployeeSerializer()
    class Meta:
        model=ServiceRequest
        fields=['id','total','invoice','service','status','persian_date_requested',
        'quantity','persian_date_added','get_edit_url','get_delete_url',
        'get_status_tag','project','employee','unit_name','unit_price','row',
        'get_absolute_url']


class MaterialRequestSerializer(serializers.ModelSerializer):
    material=MaterialSerializer()
    invoice=InvoiceSerializer()
    project=ProjectSerializer()
    employee=EmployeeSerializer()
    class Meta:
        model=Request
        fields=['id','invoice','total','material','persian_date_requested','status',
        'quantity','persian_date_added','get_edit_url','get_delete_url',
        'get_status_tag','project','employee','unit_name','unit_price','row',
        'get_absolute_url']


class MaterialRequestFullSerializer(serializers.ModelSerializer):
    material=MaterialSerializer()
    invoice=InvoiceSerializer()
    project=ProjectSerializer()
    employee=EmployeeSerializer()
    class Meta:
        model=Request
        fields=['id','invoice','total','material','persian_date_requested','status',
        'quantity','persian_date_added','get_edit_url','get_delete_url',
        'get_status_tag','project','employee','unit_name','unit_price','row',
        'get_absolute_url']
