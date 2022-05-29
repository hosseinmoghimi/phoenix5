from rest_framework import serializers
from authentication.serializers import ProfileSerializer
from organization.models import Employee,OrganizationUnit,Letter,LetterSent
from accounting.serializers import AccountSerializer


class OrganizationUnitSerializer(serializers.ModelSerializer):
    account=AccountSerializer()
    class Meta:
        model=OrganizationUnit
        fields=['id','title','full_title','account','image','logo','full_title','pre_title','get_edit_url','get_absolute_url']



class EmployeeSerializer(serializers.ModelSerializer):
    account=AccountSerializer()
    organization_unit=OrganizationUnitSerializer()
    class Meta:
        model=Employee
        fields=['id','organization_unit','job_title','get_absolute_url','get_delete_url','get_edit_url','account','title']


class LetterSerializer(serializers.ModelSerializer):
    class Meta:
        model=Letter
        fields=['id','thumbnail','title','get_absolute_url','persian_date_added','get_edit_url']


class LetterSentSerializer(serializers.ModelSerializer):
    letter=LetterSerializer()
    sender=OrganizationUnitSerializer()
    recipient=OrganizationUnitSerializer()
    profile=ProfileSerializer()
    class Meta:
        model=LetterSent
        fields=['id','letter','sender','paraf','profile','persian_date_sent','recipient','get_edit_url','get_delete_url']
 