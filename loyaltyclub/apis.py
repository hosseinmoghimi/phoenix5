from utility.calendar import PersianCalendar
from .serializers import OrderSerializer,CouponSerializer
from rest_framework.views import APIView
from .repo import OrderRepo
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
            (result,message,order,coupon)=OrderRepo(request=request).add_order(**cd)
            if result==SUCCEED:
                context['order']=OrderSerializer(order).data
                context['coupon']=CouponSerializer(coupon).data
            context['result']=result
            context['message']=message
        return JsonResponse(context)
