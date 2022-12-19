from utility.calendar import PersianCalendar
from .serializers import OrderSerializer,CouponSerializer,CoefSerializer
from rest_framework.views import APIView
from .repo import OrderRepo,CoefRepo
from .forms import *
from django.http import JsonResponse
from core.constants import FAILED,SUCCEED

class AddOrderView(APIView):
    def post(self,request,*args, **kwargs):
        context={}
        context['result']=FAILED
        AddOrderForm_=AddOrderForm(request.POST)
        if AddOrderForm_.is_valid():
            cd=AddOrderForm_.cleaned_data
            cd['date_ordered']=PersianCalendar().to_gregorian(cd['date_ordered'])
            (result,message,order,coupons)=OrderRepo(request=request).add_order(**cd)
            if result==SUCCEED:
                context['order']=OrderSerializer(order).data
                context['coupons']=CouponSerializer(coupons,many=True).data 

                

            context['result']=result
            context['message']=message
        return JsonResponse(context)



class AddInvoiceToOrderView(APIView):
    def post(self,request,*args, **kwargs):
        context={}
        context['result']=FAILED
        AddInvoiceToOrderForm_=AddInvoiceToOrderForm(request.POST)
        if AddInvoiceToOrderForm_.is_valid():
            cd=AddInvoiceToOrderForm_.cleaned_data
            (result,message,order)=OrderRepo(request=request).add_invoice_to_order(**cd)
            if result==SUCCEED:
                context['order']=OrderSerializer(order).data

                

            context['result']=result
            context['message']=message
        return JsonResponse(context)



class ChangeCoefView(APIView):
    def post(self,request,*args, **kwargs):
        context={}
        context['result']=FAILED
        ChangeCoefForm_=ChangeCoefForm(request.POST)
        if ChangeCoefForm_.is_valid():
            cd=ChangeCoefForm_.cleaned_data
            coef=CoefRepo(request=request).change_coef(**cd)
            if coef is not None: 
                context['coef']=CoefSerializer(coef).data
                result=SUCCEED
            context['result']=result 
        return JsonResponse(context)


