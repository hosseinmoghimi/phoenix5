from django.contrib import admin

from organization.models import Employee, OrganizationUnit

# Register your models here.

admin.site.register(Employee)
admin.site.register(OrganizationUnit)