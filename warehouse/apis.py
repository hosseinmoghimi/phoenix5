import json
from signal import signal
from accounting.repo import ProductRepo
from core.constants import FAILED,SUCCEED
from rest_framework.views import APIView
from warehouse.enums import *

from utility.calendar import PersianCalendar
from warehouse.repo import   WareHouseRepo, WareHouseSheetRepo, WareHouseSheetSignatureRepo
from django.http import JsonResponse
from warehouse.forms import *
from warehouse.serializers import WareHouseSerializer, WareHouseSheetSerializer, WareHouseSheetSignatureSerializer
 

class WareHouseSheetApi(APIView):
    def post(self,request,*args, **kwargs):
        context={}
        log=11
        context['result']=FAILED
        if request.method=='POST':
            log=22
            change_warehouse_sheet_state_form=ChangeWarehouseSheetStateForm(request.POST)

            if change_warehouse_sheet_state_form.is_valid():
                log=33
                fm=change_warehouse_sheet_state_form.cleaned_data
                status=fm['status']
                if status=='DONE':
                    status=WareHouseSheetStatusEnum.DONE
                elif status=='INITIAL':
                    status=WareHouseSheetStatusEnum.INITIAL
                elif status=='IN_PROGRESS':
                    status=WareHouseSheetStatusEnum.IN_PROGRESS
                else:
                    status=WareHouseSheetStatusEnum.INITIAL

                warehouse_sheet_id=fm['warehouse_sheet_id']
                warehouse_sheet=WareHouseSheetRepo(request=request).change_state(
                    warehouse_sheet_id=warehouse_sheet_id,
                    status=status,
                )
                if warehouse_sheet is not None:
                    context['warehouse_sheet']=WareHouseSheetSerializer(warehouse_sheet).data
                    context['result']=SUCCEED
        context['log']=log
        return JsonResponse(context)

class ReportApi(APIView):
    def post(self,request,*args, **kwargs):
        context={}
        log=11
        context['result']=FAILED
        if request.method=='POST':
            log=22
            report_form=ReportForm(request.POST)
            availables_list=[]
            if report_form.is_valid():
                log=33
                cd=report_form.cleaned_data
                warehouse_sheets=WareHouseSheetRepo(request=request).list(**cd)
                products=ProductRepo(request=request).list()
                for product in products:
                    warehouse_sheets_=warehouse_sheets.filter(invoice_line__product_or_service_id=product.id)
                    if len(warehouse_sheets_)>0:
                        list_item={}
                        unit_names=[]
                        for a in warehouse_sheets_:
                            if not a.invoice_line.unit_name in unit_names:
                                unit_names.append(a.invoice_line.unit_name)
                        for unit_name in unit_names:
                            list_item['product']={'id':product.pk,'title':product.title,'get_absolute_url':product.get_absolute_url()}
                            list_item['unit_name']=unit_name
                            warehouse_sheets_=warehouse_sheets_.filter(invoice_line__unit_name=unit_name)
                            available=0
                            for line in warehouse_sheets_:
                                ware_house=line.ware_house
                                available+=line.available
                        list_item['ware_house']=WareHouseSerializer(ware_house).data
                        list_item['available']=available
                        availables_list.append(list_item)
                        
                    context['availables_list']=availables_list
                    context['result']=SUCCEED
        context['log']=log
        return JsonResponse(context)

class AddWareHouseApi(APIView):
    def post(self,request,*args, **kwargs):
        context={}
        log=11
        context['result']=FAILED
        if request.method=='POST':
            log=22
            report_form=AddWarehouseForm(request.POST)
            availables_list=[]
            if report_form.is_valid():
                log=33
                cd=report_form.cleaned_data
            
                ware_house=WareHouseRepo(request=request).add_ware_house(**cd)
                if ware_house is not None:
                    context['warehouse']=WareHouseSerializer(ware_house).data
                    context['result']=SUCCEED
        context['log']=log
        return JsonResponse(context)


class AddSignatureApi(APIView):
    def post(self,request,*args, **kwargs):
        context={}
        log=11
        context['result']=FAILED
        if request.method=='POST':
            log=22
            report_form=AddSignatureForm(request.POST)
            availables_list=[]
            if report_form.is_valid():
                log=33
                cd=report_form.cleaned_data
            
                signature=WareHouseSheetSignatureRepo(request=request).add_signature(**cd)
                if signature is not None:
                    context['ware_house_sheet_signature']=WareHouseSheetSignatureSerializer(signature).data
                    context['result']=SUCCEED
        context['log']=log
        return JsonResponse(context)

class AddWareHouseSheetApi(APIView):
    def post(self,request,*args, **kwargs):
        context={}
        log=11
        context['result']=FAILED
        if request.method=='POST':
            log=22
            report_form=AddWarehouseSheetForm(request.POST)
            availables_list=[]
            if report_form.is_valid():
                log=33
                cd=report_form.cleaned_data
            
                warehouse_sheet=WareHouseSheetRepo(request=request).add_ware_house_sheet(**cd)
                if warehouse_sheet is not None:
                    context['warehouse_sheet']=WareHouseSheetSerializer(warehouse_sheet).data
                    context['result']=SUCCEED
        context['log']=log
        return JsonResponse(context)



class AddWareHouseSheetsForInvoiceApi(APIView):
    def post(self,request,*args, **kwargs):
        context={}
        log=11
        context['result']=FAILED
        if request.method=='POST':
            log=22
            report_form=AddWarehouseSheetsForInvoiceForm(request.POST)
            availables_list=[]
            if report_form.is_valid():
                log=33
                cd=report_form.cleaned_data
                warehouse_sheets=WareHouseSheetRepo(request=request).add_ware_house_sheets_for_invoice(**cd)
                if warehouse_sheets is not None:
                    context['warehouse_sheets']=WareHouseSheetSerializer(warehouse_sheets,many=True).data
                    context['result']=SUCCEED
        context['log']=log
        return JsonResponse(context)


