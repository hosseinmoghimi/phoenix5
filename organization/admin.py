from django.contrib import admin

from organization.models import Employee, Letter, OrganizationUnit, letterSent

# Register your models here.

admin.site.register(Employee)
admin.site.register(OrganizationUnit)
admin.site.register(Letter)
admin.site.register(letterSent)