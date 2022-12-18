from django.shortcuts import render
from .apps import APP_NAME
from django.http import Http404
from django.views import View
from core.views import CoreContext
from core.repo import ParameterRepo
from market.serializers import CustomerSerializer,SupplierSerializer
from market.repo import CustomerRepo,SupplierRepo
from .serializers import CustomerSerializer
from market.forms import AddCustomerForm
from .forms import *
from map.repo import AreaRepo
from .serializers import OrderSerializer,CouponSerializer,CoefSerializer
from .repo import OrderRepo,CouponRepo,CoefRepo
import json
LAYOUT_PARENT="phoenix/layout.html"

TEMPLATE_ROOT="loyaltyclub/"

def get_add_order_context(request,*args, **kwargs):
    context={}
    context['add_order_form']=AddOrderForm()

    customers=CustomerRepo(request=request).list()
    context['customers']=customers
    context['customers_s']=json.dumps(CustomerSerializer(customers,many=True).data)
    suppliers=SupplierRepo(request=request).list()
    context['suppliers']=suppliers
    context['suppliers_s']=json.dumps(SupplierSerializer(suppliers,many=True).data)
    return context

def getContext(request,*args, **kwargs):
    context=CoreContext(request=request,app_name=APP_NAME)
    context['LAYOUT_PARENT']=LAYOUT_PARENT
    # context['APP_NAME']=APP_NAME
    return context
    
class IndexView(View):
    def get(self,request,*args, **kwargs):
        context=getContext(request)
        parameter_repo=ParameterRepo(request=request,app_name=APP_NAME)
        context['card_title']=parameter_repo.parameter(name="عنوان کارت ایندکس",default="باشگاه مشتریان")

        return render(request,TEMPLATE_ROOT+"index.html",context)

class CustomersView(View):
    def get(self, request, *args, **kwargs):
        context = getContext(request)
        customer_repo=CustomerRepo(request=request)
        customers=customer_repo.list(*args,**kwargs)
         

        context['customers'] = customers
        customers_s = json.dumps(CustomerSerializer(customers,many=True).data)
        context['customers_s'] = customers_s
        context['body_class'] = "ecommerce-page"
        if request.user.has_perm(APP_NAME+".add_customer"):
            from accounting.views import add_from_accounts_context
            context['add_customer_form']=AddCustomerForm()
            context.update(add_from_accounts_context(request=request))
            context['regions']=AreaRepo(request=request).list()
        return render(request, TEMPLATE_ROOT+"customers.html", context)


class CustomerView(View):
    def get(self, request, *args, **kwargs):
        context = getContext(request)
        customer_repo=CustomerRepo(request=request)
        customer=customer_repo.customer(*args,**kwargs)
         
        context['customer'] = customer
        orders=OrderRepo(request=request).list(customer_id=customer.id)
        context['orders'] = orders
        orders_s=json.dumps(OrderSerializer(orders,many=True).data)
        context['orders_s'] = orders_s
         
        # percentage=CoefRepo(request=request).coef(number=len(orders)+1).percentage
        # context['percentage'] = percentage

        coupon_repo=CouponRepo(request=request)

        coupons=coupon_repo.list(customer_id=customer.id)
        context['coupons'] = coupons
        coupons_s=json.dumps(CouponSerializer(coupons,many=True).data)
        context['coupons_s'] = coupons_s



        coupons_sum=coupon_repo.sum(customer_id=customer.id)
        context['coupons_sum'] = coupons_sum


        context['body_class'] = "product-page"
        if request.user.has_perm(APP_NAME+".add_order"):
            # context['add_brand_form'] = AddBrandForm()
            context.update(get_add_order_context(request=request))

        return render(request, TEMPLATE_ROOT+"customer.html", context)



class SuppliersView(View):
    def get(self, request, *args, **kwargs):
        context = getContext(request)
        customer_repo=CustomerRepo(request=request)
        customers=customer_repo.list(*args,**kwargs)
         

        context['customers'] = customers
        customers_s = json.dumps(CustomerSerializer(customers,many=True).data)
        context['customers_s'] = customers_s
        context['body_class'] = "ecommerce-page"
        if request.user.has_perm(APP_NAME+".add_customer"):
            from accounting.views import add_from_accounts_context
            context['add_customer_form']=AddCustomerForm()
            context.update(add_from_accounts_context(request=request))
            context['regions']=AreaRepo(request=request).list()
        return render(request, TEMPLATE_ROOT+"suppliers.html", context)


class SupplierView(View):
    def get(self, request, *args, **kwargs):
        context = getContext(request)
        customer_repo=CustomerRepo(request=request)
        customer=customer_repo.customer(*args,**kwargs)
         

        context['customer'] = customer
        orders=OrderRepo(request=request).list(customer_id=customer.id)
        context['orders'] = orders
        orders_s=json.dumps(OrderSerializer(orders,many=True).data)
        context['orders_s'] = orders_s
         
        context['body_class'] = "product-page"
        if request.user.has_perm(APP_NAME+".add_order"):
            # context['add_brand_form'] = AddBrandForm()
            context.update(get_add_order_context(request=request))

        return render(request, TEMPLATE_ROOT+"supplier.html", context)



 

class CouponView(View):
    def get(self, request, *args, **kwargs):
        context = getContext(request)
        customer_repo=CustomerRepo(request=request)
        customer=customer_repo.customer(*args,**kwargs)
         

        context['customer'] = customer
        coupon=CouponRepo(request=request).coupon(*args, **kwargs)
        context['coupon'] = coupon
        coupon_s=json.dumps(CouponSerializer(coupon).data)
        context['coupon_s'] = coupon_s
         
        context['body_class'] = "product-page"
        if request.user.has_perm(APP_NAME+".add_order"):
            # context['add_brand_form'] = AddBrandForm()
            context.update(get_add_order_context(request=request))

        return render(request, TEMPLATE_ROOT+"coupon.html", context)




class CouponsView(View):
    def get(self, request, *args, **kwargs):
        context = getContext(request)
        customer_repo=CustomerRepo(request=request)
        customer=customer_repo.customer(*args,**kwargs)
         

        context['customer'] = customer
        coupons=CouponRepo(request=request).list(customer_id=customer.id)
        context['coupons'] = coupons
        coupons_s=json.dumps(CouponSerializer(coupons,many=True).data)
        context['coupons_s'] = coupons_s
         
        context['body_class'] = "product-page"
        if request.user.has_perm(APP_NAME+".add_order"):
            # context['add_brand_form'] = AddBrandForm()
            context.update(get_add_order_context(request=request))

        return render(request, TEMPLATE_ROOT+"coupons.html", context)




class CoefsView(View):
    def get(self, request, *args, **kwargs):
        context = getContext(request)
        
 
        coefs=CoefRepo(request=request).list()
        context['coefs'] = coefs
        coefs_s=json.dumps(CoefSerializer(coefs,many=True).data)
        context['coefs_s'] = coefs_s
         
        context['body_class'] = "product-page"
        if request.user.has_perm(APP_NAME+".add_order"):
            # context['add_brand_form'] = AddBrandForm()
            context.update(get_add_order_context(request=request))

        return render(request, TEMPLATE_ROOT+"coefs.html", context)




class OrdersView(View):
    def get(self, request, *args, **kwargs):
        context = getContext(request)
        customer_repo=CustomerRepo(request=request)
        customers=customer_repo.list(*args,**kwargs)
         

        context['customers'] = customers
        customers_s = json.dumps(CustomerSerializer(customers,many=True).data)
        context['customers_s'] = customers_s
        context['body_class'] = "ecommerce-page"
        if request.user.has_perm(APP_NAME+".add_customer"):
            from accounting.views import add_from_accounts_context
            context['add_customer_form']=AddCustomerForm()
            context.update(add_from_accounts_context(request=request))
            context['regions']=AreaRepo(request=request).list()
        return render(request, TEMPLATE_ROOT+"orders.html", context)


class OrderView(View):
    def get(self, request, *args, **kwargs):
        context = getContext(request)
        customer_repo=CustomerRepo(request=request)
        customer=customer_repo.customer(*args,**kwargs)
         

        context['customer'] = customer
        orders=OrderRepo(request=request).list(customer_id=customer.id)
        context['orders'] = orders
        orders_s=json.dumps(OrderSerializer(orders,many=True).data)
        context['orders_s'] = orders_s
         
        context['body_class'] = "product-page"
        if request.user.has_perm(APP_NAME+".add_brand"):
            # context['add_brand_form'] = AddBrandForm()
            pass

        return render(request, TEMPLATE_ROOT+"order.html", context)

