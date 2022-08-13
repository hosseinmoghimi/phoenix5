from requests import request
from map.models import PageLocation
from map.repo import LocationRepo
from scheduler.models import Appointment,APP_NAME
from authentication.repo import ProfileRepo
from django.utils import timezone


class AppointmentRepo():
    def __init__(self, *args, **kwargs):
        self.request = None
        self.user = None
        if 'request' in kwargs:
            self.request = kwargs['request']
            self.user = self.request.user
        if 'user' in kwargs:
            self.user = kwargs['user']
        
        self.objects=Appointment.objects.all()
        self.profile=ProfileRepo(*args, **kwargs).me

    def appointment(self, *args, **kwargs):
        pk=0
        if 'appointment_id' in kwargs:
            pk=kwargs['appointment_id']
        elif 'pk' in kwargs:
            pk=kwargs['pk']
        elif 'id' in kwargs:
            pk=kwargs['id']
        return self.objects.filter(pk=pk).first()
     
    def list(self, *args, **kwargs):
        objects = self.objects.all()
        if 'search_for' in kwargs:
            search_for=kwargs['search_for']
            objects = objects.filter(Q(title__contains=search_for)|Q(short_description__contains=search_for)|Q(description__contains=search_for))
        if 'for_home' in kwargs:
            objects = objects.filter(Q(for_home=kwargs['for_home']))
        if 'parent_id' in kwargs:
            objects=objects.filter(parent_id=kwargs['parent_id'])
        return objects.all()

    def add_appointment(self,*args, **kwargs):
        if not self.user.has_perm(APP_NAME+".add_appointment"):
            return
        location_id=0
        if 'location_id' in kwargs:
            location_id=kwargs['location_id']
            del kwargs['location_id']
        appointment=Appointment(*args, **kwargs)
        appointment.save()

        if location_id>0:
            # location=LocationRepo(request=self.request).location(pk=location_id)
            # if location is not None:
            page_location=PageLocation(page_id=appointment.pk,location_id=location_id)
            page_location.save()

        print("kwargs")
        print(kwargs)
        print(100*"#")
        return appointment
