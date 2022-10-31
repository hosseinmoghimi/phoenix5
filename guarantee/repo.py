from email import message
from operator import inv
from core.constants import FAILED,SUCCEED
from accounting.repo import InvoiceLineRepo, InvoiceRepo
from django.db.models import Q
from authentication.repo import ProfileRepo
from django.utils import timezone
from utility.log import leolog
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
        if 'invoice_line_id' in kwargs:
            objects = objects.filter(invoice_line_id=kwargs['invoice_line_id'])
        if 'product_id' in kwargs:
            objects = objects.filter(invoice_line__product_or_service_id=kwargs['product_id'])
        if 'invoice_id' in kwargs:
            objects = objects.filter(invoice_line__invoice_id=kwargs['invoice_id'])
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

    def add(self,*args, **kwargs):
        result=FAILED
        guarantee=None
        message=""
        if not self.request.user.has_perm(APP_NAME+".add_guarantee"):
            return result,message,guarantee
        invoice_line=InvoiceLineRepo(request=self.request,*args, **kwargs)
        if invoice_line is None:
            result=FAILED
            return result,message,guarantee

        guarantee=Guarantee(*args, **kwargs)
        guarantee.save()
        result=SUCCEED
        message="با موفقیت افزوده شد."
        return result,message,guarantee
 