from django.utils import timezone
from .models import Order
from authentication.repo import ProfileRepo
from .apps import APP_NAME
from core.constants import FAILED,SUCCEED
from django.db.models import Q

class OrderRepo():  
    def __init__(self, *args, **kwargs):
        self.request = None
        self.user = None
        self.me = None
        if 'request' in kwargs:
            self.request = kwargs['request']
            self.user = self.request.user
        if 'user' in kwargs:
            self.user = kwargs['user']
        
        self.objects=Order.objects.all()
        self.profile=ProfileRepo(*args, **kwargs).me
        # self.account=AccountRepo(request=request).me
        if self.profile is not None:
            # self.me=Customer.objects.filter(account__profile_id=self.profile.id).first()
            pass
       

    def order(self, *args, **kwargs):
        pk=0
        if 'order_id' in kwargs:
            pk= kwargs['order_id']
            return self.objects.filter(pk=pk).first()
       
        elif 'pk' in kwargs:
            pk=kwargs['pk']
            return self.objects.filter(pk=pk).first()
        elif 'id' in kwargs:
            pk=kwargs['id']
            return self.objects.filter(pk=pk).first()
     
    def add_order(self,*args, **kwargs):
        result=FAILED
        message=""
        order=None
        if not self.request.user.has_perm(APP_NAME+".add_order"):
            return
        customer_id=kwargs['customer_id']
        supplier_id=kwargs['supplier_id']
        title=kwargs['title']
        discount=0
        ship_fee=0
        date_ordered=timezone.now()
        if 'date_ordered' in kwargs:
            date_ordered=kwargs['date_ordered']
        if 'ship_fee' in kwargs:
            ship_fee=kwargs['ship_fee']
        if 'discount' in kwargs:
            discount=kwargs['discount']
        
        invoice_id_=kwargs['invoice_id']
        invoice_id=0
        if invoice_id_ is not None and invoice_id_>0:
            invoice_id=invoice_id_
        sum=kwargs['sum']
        # order=Order.objects.filter(customer_id=customer_id).first()
       
        order=Order()
        order.supplier_id=supplier_id
        order.customer_id=customer_id
        if invoice_id>0:
            order.invoice_id=invoice_id
        order.sum=sum
        order.title=title
        order.ship_fee=ship_fee
        order.discount=discount
        order.date_ordered=date_ordered
        order.save()
        if order is not None:
            result=SUCCEED
            message="سفارش جدید با موفقیت افزوده شد."
        return result,message,order

    
    def list(self, *args, **kwargs):
        objects = self.objects
        if 'search_for' in kwargs:
            search_for=kwargs['search_for']
            objects = objects.filter(Q(title__contains=search_for)|Q(short_description__contains=search_for)|Q(description__contains=search_for))
        if 'for_home' in kwargs:
            objects = objects.filter(Q(for_home=kwargs['for_home']))
        if 'parent_id' in kwargs:
            objects=objects.filter(parent_id=kwargs['parent_id'])
        if 'customer_id' in kwargs:
            objects=objects.filter(customer_id=kwargs['customer_id'])
        return objects.all()

