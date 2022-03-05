from django.contrib import admin

from projectmanager.models import Employee,  MaterialInvoice, OrganizationUnit, Project, Request, RequestSignature, SampleForm,  ServiceInvoice

# Register your models here.
admin.site.register(OrganizationUnit)
admin.site.register(Employee)
admin.site.register(Project)
admin.site.register(Request)
admin.site.register(MaterialInvoice)
admin.site.register(ServiceInvoice)
admin.site.register(RequestSignature)
admin.site.register(SampleForm)
