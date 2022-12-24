from django.shortcuts import render
from .apps import APP_NAME
from django.http import Http404
from accounting.views import get_account_context
from django.views import View
from core.views import CoreContext,PageContext
from core.repo import ParameterRepo
from market.serializers import CustomerSerializer,SupplierSerializer
from market.repo import CustomerRepo,SupplierRepo
from .serializers import CustomerSerializer
from market.forms import AddCustomerForm,AddSupplierForm
from .forms import *
from map.repo import AreaRepo
from .serializers import OrderSerializer,CouponSerializer,CoefSerializer
from .repo import OrderRepo,CouponRepo,CoefRepo
import json
from accounting.views import get_transaction_context
LAYOUT_PARENT="phoenix/layout.html"

TEMPLATE_ROOT="loyaltyclub/"
from market.views import get_customer_context,get_supplier_context

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
        from .repo import normalize_coupons
        normalize_coupons(customer_id=customer.id)
        context.update(get_customer_context(request=request,customer=customer))

        coupon_repo=CouponRepo(request=request)
        # payment_repo=PaymentRepo(request=request)
        order_repo=OrderRepo(request=request)

        context['customer'] = customer
        orders=order_repo.list(customer_id=customer.id)
        context['orders'] = orders
        orders_s=json.dumps(OrderSerializer(orders,many=True).data)
        context['orders_s'] = orders_s
         
        # percentage=CoefRepo(request=request).coef(number=len(orders)+1).percentage
        # context['percentage'] = percentage
        coupons=coupon_repo.list(customer_id=customer.id)
        context['coupons'] = coupons
        coupons_s=json.dumps(CouponSerializer(coupons,many=True).data)
        context['coupons_s'] = coupons_s



        coupons_count,coupons_sum=coupon_repo.sum(customer_id=customer.id)
        orders_sum,discounts,paids,ship_fees=order_repo.sum(customer_id=customer.id)
        context['orders_sum'] = orders_sum
        context['paids'] = paids
        context['ship_fees'] = ship_fees
        context['discounts'] = discounts
        context['coupons_sum'] = coupons_sum
        context['coupons_count'] = coupons_count

        coupons_remain=coupons_sum-discounts
        context['coupons_remain'] = coupons_remain


        context['body_class'] = "product-page"
        if request.user.has_perm(APP_NAME+".add_order"):
            # context['add_brand_form'] = AddBrandForm()
            context.update(get_add_order_context(request=request))

        return render(request, TEMPLATE_ROOT+"customer.html", context)



class SuppliersView(View):
    def get(self, request, *args, **kwargs):
        context = getContext(request)
        supplier_repo=SupplierRepo(request=request)
        suppliers=supplier_repo.list(*args,**kwargs)
         

        context['suppliers'] = suppliers
        suppliers_s = json.dumps(SupplierSerializer(suppliers,many=True).data)
        context['suppliers_s'] = suppliers_s
        context['body_class'] = "ecommerce-page"
        if request.user.has_perm(APP_NAME+".add_supplier"):
            from accounting.views import add_from_accounts_context
            context['add_supplier_form']=AddSupplierForm()
            context.update(add_from_accounts_context(request=request))
            context['regions']=AreaRepo(request=request).list()
        return render(request, TEMPLATE_ROOT+"suppliers.html", context)


class SupplierView(View):
    def get(self, request, *args, **kwargs):
        context = getContext(request)
        supplier_repo=SupplierRepo(request=request)
        supplier=supplier_repo.supplier(*args,**kwargs)
        context.update(get_supplier_context(request=request,supplier=supplier))

        context['supplier'] = supplier
        orders=OrderRepo(request=request).list(supplier_id=supplier.id)
        context['orders'] = orders
        orders_s=json.dumps(OrderSerializer(orders,many=True).data)
        context['orders_s'] = orders_s
         
        coupon_repo=CouponRepo(request=request)
        coupons=coupon_repo.list(supplier_id=supplier.id)
         

        context['coupons'] = coupons
        context['coupons'] = coupons
        coupons_s=json.dumps(CouponSerializer(coupons,many=True).data)
        context['coupons_s'] = coupons_s


        order_repo=OrderRepo(request=request)
        coupons_sum=coupon_repo.sum(supplier_id=supplier.id)
        orders_sum,discounts,paids,ship_fees=order_repo.sum(supplier_id=supplier.id)
        context['orders_sum'] = orders_sum
        context['paids'] = paids
        context['ship_fees'] = ship_fees
        context['discounts'] = discounts
        context['coupons_sum'] = coupons_sum


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
        context.update(get_transaction_context(request=request,transaction=coupon))
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
        coupon_repo=CouponRepo(request=request)
        coupons=coupon_repo.list(*args,**kwargs)
         

        context['coupons'] = coupons
        context['coupons'] = coupons
        coupons_s=json.dumps(CouponSerializer(coupons,many=True).data)
        context['coupons_s'] = coupons_s
         
        context['body_class'] = "product-page"
        if request.user.has_perm(APP_NAME+".add_order"):
            # context['add_brand_form'] = AddBrandForm()
            context.update(get_add_order_context(request=request))

        return render(request, TEMPLATE_ROOT+"coupons.html", context)




class DiscountPayView(View):
    def get(self, request, *args, **kwargs):
        context = getContext(request)
        customer_repo=CustomerRepo(request=request)
        customer=customer_repo.customer(*args,**kwargs)
         

        context['customer'] = customer
        coupon=CouponRepo(request=request).coupon(*args, **kwargs)
        context['coupon'] = coupon
        context.update(get_transaction_context(request=request,transaction=coupon))
        coupon_s=json.dumps(CouponSerializer(coupon).data)
        context['coupon_s'] = coupon_s
         
        context['body_class'] = "product-page"
        if request.user.has_perm(APP_NAME+".add_order"):
            # context['add_brand_form'] = AddBrandForm()
            context.update(get_add_order_context(request=request))

        return render(request, TEMPLATE_ROOT+"coupon.html", context)




class DiscountPaysView(View):
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
        order_repo=OrderRepo(request=request)
        orders=order_repo.list(*args,**kwargs)
         

        context['orders'] = orders
        orders_s = json.dumps(OrderSerializer(orders,many=True).data)
        context['orders_s'] = orders_s

        
      


        context['body_class'] = "ecommerce-page"
        
        return render(request, TEMPLATE_ROOT+"orders.html", context)


class OrderView(View):
    def get(self, request, *args, **kwargs):
        context = getContext(request)
        order_repo=OrderRepo(request=request)
        order=order_repo.order(*args,**kwargs)
         

        context['order'] = order
 
         
        context['body_class'] = "product-page"
        if request.user.has_perm(APP_NAME+".change_order"):
            # context['add_brand_form'] = AddBrandForm()
            context['add_invoice_to_order_form']=AddInvoiceToOrderForm()

        return render(request, TEMPLATE_ROOT+"order.html", context)

