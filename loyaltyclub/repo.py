from django.utils import timezone
from .models import Order,Coupon
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
        coupon=None
        if not self.request.user.has_perm(APP_NAME+".add_order"):
            return result,message,order,coupon
            
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
        if 'coupon' in kwargs and kwargs['coupon'] is not None and kwargs['coupon']>0:
            coupon=Coupon()
            coupon.order=order
            coupon.amount=kwargs['coupon']
            coupon.save()

        if order is not None:
            result=SUCCEED
            message="سفارش جدید با موفقیت افزوده شد."
        return result,message,order,coupon

    
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




class CouponRepo():  
    def __init__(self, *args, **kwargs):
        self.request = None
        self.user = None
        self.me = None
        if 'request' in kwargs:
            self.request = kwargs['request']
            self.user = self.request.user
        if 'user' in kwargs:
            self.user = kwargs['user']
        
        self.objects=Coupon.objects.all()
        self.profile=ProfileRepo(*args, **kwargs).me
        # self.account=AccountRepo(request=request).me
        if self.profile is not None:
            # self.me=Customer.objects.filter(account__profile_id=self.profile.id).first()
            pass
       


    def sum(self, *args, **kwargs):
        sum=0
        customer_id=0

        if 'customer_id' in kwargs and kwargs['customer_id'] is not None:
            customer_id=kwargs['customer_id']

        coupons=Coupon.objects
        if customer_id>0:
            coupons=coupons.filter(order__customer_id=customer_id)

        for coupon in coupons:
            sum+=coupon.amount

        return sum


    def coupon(self, *args, **kwargs):
        pk=0
        if 'coupon_id' in kwargs:
            pk= kwargs['coupon_id']
            return self.objects.filter(pk=pk).first()
       
        elif 'pk' in kwargs:
            pk=kwargs['pk']
            return self.objects.filter(pk=pk).first()
        elif 'id' in kwargs:
            pk=kwargs['id']
            return self.objects.filter(pk=pk).first()
     
    def add_coupon(self,*args, **kwargs):
        result=FAILED
        message=""
        coupon=None
        if not self.request.user.has_perm(APP_NAME+".add_coupon"):
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
        # coupon=Order.objects.filter(customer_id=customer_id).first()
       
        coupon=Order()
        coupon.supplier_id=supplier_id
        coupon.customer_id=customer_id
        if invoice_id>0:
            coupon.invoice_id=invoice_id
        coupon.sum=sum
        coupon.title=title
        coupon.ship_fee=ship_fee
        coupon.discount=discount
        coupon.date_ordered=date_ordered
        coupon.save()
        if coupon is not None:
            result=SUCCEED
            message="کوپن جدید با موفقیت افزوده شد."
        return result,message,coupon

    
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
            objects=objects.filter(order__customer_id=kwargs['customer_id'])
        return objects.all()

