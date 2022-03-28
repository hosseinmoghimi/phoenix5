from django.http import Http404, JsonResponse
from django.shortcuts import render,reverse
from core.constants import CURRENCY, FAILED, SUCCEED 
from core.views import CoreContext, PageContext,SearchForm
# Create your views here.
from django.views import View

from utility.calendar import PersianCalendar
from warehouse.repo import WareHouseRepo, WareHouseSheetRepo
from warehouse.serializers import WareHouseSerializer, WareHouseSheetSerializer
from .apps import APP_NAME
# 
import json
from accounting.repo import ProductRepo

LAYOUT_PARENT = "phoenix/layout.html"
TEMPLATE_ROOT = APP_NAME+"/"


def getContext(request, *args, **kwargs):
    context = CoreContext(request=request, app_name=APP_NAME)
    # context['search_form'] = SearchForm()
    # context['search_action'] = reverse(APP_NAME+":search")
    context['LAYOUT_PARENT'] = LAYOUT_PARENT
    return context
 
class HomeView(View):
    def get(self,request,*args, **kwargs):
        # context=getContext(request=request)
        # return render(request,TEMPLATE_ROOT+"index.html",context)
        return WareHousesViews().get(request=request,*args, **kwargs)


class WareHouseViews(View):
    def get(self,request,*args, **kwargs):
        context=getContext(request=request)
        ware_house=WareHouseRepo(request=request).ware_house(*args, **kwargs)
        context['ware_house']=ware_house
        
        warehouse_sheets=WareHouseSheetRepo(request=request).list(ware_house_id=ware_house.id).order_by('date_registered')
        warehouse_sheets_s=json.dumps(WareHouseSheetSerializer(warehouse_sheets,many=True).data)
        context['warehouse_sheets_s']=warehouse_sheets_s


        products=ProductRepo(request=request).list()
        availables_list=[]
        for product in products:    
            line=warehouse_sheets.filter(product_id=product.id).filter(ware_house=ware_house).first()
            if line is not None:
                list_item={'product':{'id':product.pk,'title':product.title,'get_absolute_url':product.get_absolute_url()}}
                list_item['available']=line.available()
                list_item['unit_name']=line.unit_name
                availables_list.append(list_item)
        context['availables_list']=json.dumps(availables_list)

        return render(request,TEMPLATE_ROOT+"ware-house.html",context)


class WareHousePrintViews(View):

    def get(self,request,*args, **kwargs):
        context=getContext(request=request)
        context['no_footer']=True
        context['no_nav_bar']=True
        ware_house=WareHouseRepo(request=request).ware_house(*args, **kwargs)
        context['ware_house']=ware_house
        
        warehouse_sheets=WareHouseSheetRepo(request=request).list(ware_house_id=ware_house.id).order_by('date_registered')
    
    

        products=ProductRepo(request=request).list()
        availables_list=[]
        for product in products:    
            line=warehouse_sheets.filter(product_id=product.id).filter(ware_house=ware_house).first()
            if line is not None:
                list_item={'product':{'id':product.pk,'title':product.title,'get_absolute_url':product.get_absolute_url()}}
                list_item['available']=line.available()
                list_item['unit_name']=line.unit_name
                availables_list.append(list_item)
        context['availables_list']=json.dumps(availables_list)

        return render(request,TEMPLATE_ROOT+"ware-house-print.html",context)


class WareHousesViews(View):
    def get(self,request,*args, **kwargs):
        context=getContext(request=request)
        ware_houses=WareHouseRepo(request=request).list(*args, **kwargs)
        context['ware_houses']=ware_houses
        ware_houses_s=json.dumps(WareHouseSerializer(ware_houses,many=True).data)
        context['ware_houses_s']=ware_houses_s
        

        return render(request,TEMPLATE_ROOT+"ware-houses.html",context)
    

class WareHouseSheetViews(View):
    def get(self,request,*args, **kwargs):
        context=getContext(request=request)
        warehouse_sheet=WareHouseSheetRepo(request=request).warehouse_sheet(*args, **kwargs)
        context['warehouse_sheet']=warehouse_sheet
        return render(request,TEMPLATE_ROOT+"ware-house-sheet.html",context)

 