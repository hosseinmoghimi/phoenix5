from django.shortcuts import render
from .apps import APP_NAME
from django.http import Http404
from django.views import View
from core.views import CoreContext
from core.repo import ParameterRepo
from market.repo import CustomerRepo
from .serializers import CustomerSerializer
from market.forms import AddCustomerForm
from map.repo import AreaRepo
from .serializers import OrderSerializer
from .repo import OrderRepo
import json
LAYOUT_PARENT="phoenix/layout.html"

TEMPLATE_ROOT="loyaltyclub/"
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
         
        context['body_class'] = "product-page"
        if request.user.has_perm(APP_NAME+".add_brand"):
            # context['add_brand_form'] = AddBrandForm()
            pass

        return render(request, TEMPLATE_ROOT+"customer.html", context)



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

