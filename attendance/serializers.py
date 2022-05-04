from rest_framework import serializers
from organization.models import Employee,OrganizationUnit
from accounting.serializers import AccountSerializer


class OrganizationUnitSerializer(serializers.ModelSerializer):

    class Meta:
        model=OrganizationUnit
        fields=['id','title','image','logo','full_title','pre_title','get_edit_url','get_absolute_url']



class EmployeeSerializer(serializers.ModelSerializer):
    account=AccountSerializer()
    organization_unit=OrganizationUnitSerializer()
    class Meta:
        model=Employee
        fields=['id','organization_unit','mobile','job_title','get_absolute_url','get_delete_url','get_edit_url','account','title']

