from rest_framework import serializers
from .models import DailyAttendance,Group,Salary,MonthlyAttendance
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

class DailyAttendanceSerializer(serializers.ModelSerializer):
    employee=EmployeeSerializer()
    class Meta:
        model=DailyAttendance
        fields=['id','status','get_absolute_url','get_delete_url','get_edit_url','employee']



class SalarySerializer(serializers.ModelSerializer):
    employee=EmployeeSerializer()
    class Meta:
        model=Salary
        fields=['id','color','direction','amount','title','year','month','month_name','get_absolute_url','get_delete_url','get_edit_url','employee']

