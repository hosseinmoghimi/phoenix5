from rest_framework import serializers
from .models import Attendance,Group,Salary
from accounting.serializers import AccountSerializer
from organization.serializers import OrganizationUnitSerializer,Employee


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model=Group
        fields=['id','type','title','get_edit_url','get_delete_url','get_absolute_url']



class EmployeeSerializer(serializers.ModelSerializer):
    account=AccountSerializer()
    organization_unit=OrganizationUnitSerializer()
    class Meta:
        model=Employee
        fields=['id','organization_unit','job_title','get_absolute_url','get_salary_url','get_delete_url','get_edit_url','account','title']

class AttendanceSerializer(serializers.ModelSerializer):
    account=AccountSerializer()
    class Meta:
        model=Attendance
        fields=['id','status','get_absolute_url','get_delete_url','get_edit_url','account']



class SalarySerializer(serializers.ModelSerializer):
    employee=EmployeeSerializer()
    class Meta:
        model=Salary
        fields=['id','color','direction','amount','title','year','month','month_name','get_absolute_url','get_delete_url','get_edit_url','employee']

