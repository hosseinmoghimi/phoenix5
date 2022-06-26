from django.http import Http404, HttpResponse, JsonResponse
from django.shortcuts import render,reverse
from django.utils import timezone
from core.constants import FAILED,SUCCEED
from utility.apps import APP_NAME
from core.views import CoreContext, MessageView, PageContext,SearchForm
# Create your views here.
from django.views import View
from utility.calendar import PersianCalendar
from utility.forms import *
import json
from phoenix.server_settings import phoenix_apps
LAYOUT_PARENT = "phoenix/layout.html"
TEMPLATE_ROOT = "utility/"


def getContext(request, *args, **kwargs):
    context = CoreContext(request=request, app_name=APP_NAME)
    context['LAYOUT_PARENT'] = LAYOUT_PARENT
    return context


class DateConverterView(View):
    def get(self,request,*args, **kwargs):
        context=getContext(request=request)
        context['datetime_form']=DateTimeForm()
        pc=PersianCalendar()
        context['gregorian_datetime']=pc.date.strftime("%Y/%m/%d %H:%M:%S")
        context['shamsi_datetime']=pc.from_gregorian(pc.date)
        return render(request,TEMPLATE_ROOT+"date-converter.html",context)

    def post(self,request,*args, **kwargs):
        context={}
        context['result']=FAILED
        datetime_form=DateTimeForm(request.POST)
        if datetime_form.is_valid():
            cd=datetime_form.cleaned_data
            gregorian_datetime_i=cd['gregorian_datetime']
            persian_datetime_i=cd['persian_datetime']

            pc=PersianCalendar()
            date=pc.date


            if gregorian_datetime_i is not None and not gregorian_datetime_i=="":
                import dateutil.parser       
                date=dateutil.parser.parse(gregorian_datetime_i)

            if persian_datetime_i is not None and not persian_datetime_i=="":
                date=pc.to_gregorian(persian_datetime_i) 
            
            gregorian_datetime=date.strftime("%Y/%m/%d %H:%M:%S")
            persian_datetime=pc.from_gregorian(greg_date_time=date)

            context['persian_datetime']=persian_datetime
            context['gregorian_datetime']=gregorian_datetime
            context['result']=SUCCEED
        return JsonResponse(context)



class ChartsView(View):
    def get(self,request,*args, **kwargs):
        context=getContext(request=request)
        
        return render(request,TEMPLATE_ROOT+"charts.html",context)

class HomeView(View):
    def get(self,request,*args, **kwargs):
        context=getContext(request=request)
        
        return render(request,TEMPLATE_ROOT+"index.html",context)
