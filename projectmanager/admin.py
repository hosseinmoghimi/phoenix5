from django.contrib import admin

from projectmanager.models import MaterialRequest,ServiceRequest,PM_Service,Employee,Material, MaterialInvoice, OrganizationUnit, Project, Request, RequestSignature, SampleForm,  ServiceInvoice

# Register your models here.
admin.site.register(OrganizationUnit)
admin.site.register(Employee)
admin.site.register(Project)
admin.site.register(Request)
admin.site.register(Material)
admin.site.register(PM_Service)
admin.site.register(MaterialInvoice)
admin.site.register(ServiceInvoice)
admin.site.register(MaterialRequest)
admin.site.register(ServiceRequest)
admin.site.register(RequestSignature)
admin.site.register(SampleForm)
