from django.contrib import admin

from projectmanager.models import Event, Letter,MaterialRequest,ServiceRequest,Employee, MaterialInvoice, OrganizationUnit, Project, Request, RequestSignature, SampleForm,  ServiceInvoice, letterSent

# Register your models here.
admin.site.register(Employee)
admin.site.register(Event)
admin.site.register(Letter)
admin.site.register(letterSent)
admin.site.register(MaterialInvoice)
admin.site.register(MaterialRequest)
admin.site.register(OrganizationUnit)
admin.site.register(Project)
admin.site.register(Request)
admin.site.register(RequestSignature)
admin.site.register(ServiceInvoice)
admin.site.register(ServiceRequest)
admin.site.register(SampleForm)
