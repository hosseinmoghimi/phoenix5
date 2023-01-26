from map.models import PageLocation
from map.repo import LocationRepo
from phoenix.constants import FAILED,SUCCEED
from scheduler.models import Appointment,APP_NAME
from authentication.repo import ProfileRepo
from django.utils import timezone
from accounting.repo import AccountRepo

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

    def add_account_to_appointment(self,*args, **kwargs):
        result=FAILED
        message=""
        appointment=None

        if not self.user.has_perm(APP_NAME+".change_appointment"):
            return
        appointment=self.appointment(*args, **kwargs)
        account=AccountRepo(request=self.request).account(*args, **kwargs)
        if account is None or appointment is None:
            result=FAILED
            message="اطلاعات وارد شده ناصحیح می باشد."
            return result,appointment,message
        
        if account in appointment.accounts.all():
            result=FAILED
            message="قبلا این اکانت به قرار ملاقات اضافه شده است."
            return result,appointment,message
        else:
            appointment.accounts.add(account)
            appointment.save()
            result=SUCCEED
            message="با موفقیت اضافه شد."
        return result,appointment,message


    def add_appointment(self,*args, **kwargs):
        if not self.user.has_perm(APP_NAME+".add_appointment"):
            return
        location_id=0
        if 'location_id' in kwargs:
            location_id=kwargs['location_id']
            del kwargs['location_id']
        appointment=Appointment(*args, **kwargs)
        appointment.save()
        appointment.profiles.add(self.profile)

        if location_id>0:
            # location=LocationRepo(request=self.request).location(pk=location_id)
            # if location is not None:
            page_location=PageLocation(page_id=appointment.pk,location_id=location_id)
            page_location.save()

        return appointment
