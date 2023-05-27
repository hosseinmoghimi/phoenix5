from django.contrib import admin

from projectmanager.models import RemoteClient,Event,MaterialRequest,ServiceRequest, MaterialInvoice, Project, Request, RequestSignature, SampleForm,  ServiceInvoice

# Register your models here.
admin.site.register(Event)
admin.site.register(MaterialInvoice)
admin.site.register(MaterialRequest)
admin.site.register(Project)
admin.site.register(Request)
admin.site.register(RequestSignature)
admin.site.register(ServiceInvoice)
admin.site.register(ServiceRequest)
admin.site.register(RemoteClient)
admin.site.register(SampleForm)
