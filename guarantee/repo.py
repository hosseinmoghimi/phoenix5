from django.db.models import Q
from authentication.repo import ProfileRepo
from django.utils import timezone

from guarantee.enums import *
from utility.calendar import PersianCalendar

from guarantee.apps import APP_NAME
from guarantee.models import Guarantee
   

 
class GuaranteeRepo:
    def __init__(self, *args, **kwargs):
        self.request = None
        self.user = None
        if 'request' in kwargs:
            self.request = kwargs['request']
            self.user = self.request.user
        if 'user' in kwargs:
            self.user = kwargs['user']
        self.objects = Guarantee.objects
        self.profile = ProfileRepo(user=self.user).me
        # self.me=Store.objects.filter(profile=self.profile).first()

    def list(self, *args, **kwargs):
        objects = self.objects.all()
        if 'for_home' in kwargs:
            objects = objects.filter(for_home=kwargs['for_home'])
        if 'invoice_id' in kwargs:
            objects = objects.filter(invoice_id=kwargs['invoice_id'])
        if 'search_for' in kwargs:
            search_for=kwargs['search_for']
            objects = objects.filter(title__contains=search_for) 
        return objects

    def guarantee(self, *args, **kwargs):
        if 'guarantee_id' in kwargs:
            return self.objects.filter(pk= kwargs['guarantee_id']).first()
        if 'pk' in kwargs:
            return self.objects.filter(pk= kwargs['pk']).first()
        if 'id' in kwargs:
            return self.objects.filter(pk= kwargs['id']).first()

 