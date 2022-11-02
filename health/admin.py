from health.models import Disease, Doctor, Drug, Patient, Visit
from django.contrib import admin
admin.site.register(Patient)
admin.site.register(Doctor)
admin.site.register(Disease)
admin.site.register(Visit)
admin.site.register(Drug)