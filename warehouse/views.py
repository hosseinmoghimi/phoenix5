#
import json
from warehouse.enums import WareHouseSheetStatusEnum

from accounting.repo import ProductRepo
from core.views import CoreContext, PageContext, SearchForm
from django.http import Http404, JsonResponse
from django.shortcuts import render, reverse
from django.views import View
from projectmanager.enums import SignatureStatusEnum
from organization.repo import EmployeeRepo
from utility.calendar import PersianCalendar

from warehouse.apps import APP_NAME
from warehouse.forms import *
from warehouse.repo import WareHouseRepo, WareHouseSheetRepo
from warehouse.serializers import (WareHouseSerializer,
                                   WareHouseSheetSerializer,
                                   WareHouseSheetSignatureSerializer)

LAYOUT_PARENT = "phoenix/layout.html"
TEMPLATE_ROOT = APP_NAME+"/"


def getContext(request, *args, **kwargs):
    context = CoreContext(request=request, app_name=APP_NAME)
    # context['search_form'] = SearchForm()
    # context['search_action'] = reverse(APP_NAME+":search")
    context['LAYOUT_PARENT'] = LAYOUT_PARENT
    return context


class HomeView(View):
    def get(self, request, *args, **kwargs):
        context=getContext(request=request)
        return render(request,TEMPLATE_ROOT+"index.html",context)


class WareHouseViews(View):
    def get(self, request, *args, **kwargs):
        context = getContext(request=request)
        ware_house = WareHouseRepo(request=request).ware_house(*args, **kwargs)
        context['ware_house'] = ware_house

        warehouse_sheets = WareHouseSheetRepo(request=request).list(
            ware_house_id=ware_house.id).order_by('date_registered')
        warehouse_sheets_s = json.dumps(
            WareHouseSheetSerializer(warehouse_sheets, many=True).data)
        context['warehouse_sheets_s'] = warehouse_sheets_s

        products = ProductRepo(request=request).list()
        availables_list = []
        for product in products:
            warehouse_sheets_ = warehouse_sheets.filter(
                invoice_line__product_or_service_id=product.id).filter(
                status=WareHouseSheetStatusEnum.DONE)
            if len(warehouse_sheets_) > 0:
                list_item = {}
                unit_names = []
                for a in warehouse_sheets_:
                    if not a.invoice_line.unit_name in unit_names:
                        unit_names.append(a.invoice_line.unit_name)
                for unit_name in unit_names:
                    list_item['ware_house'] = WareHouseSerializer(
                        ware_house).data
                    list_item['product'] = {
                        'id': product.pk, 'title': product.title, 'get_absolute_url': product.get_absolute_url()}
                    list_item['unit_name'] = unit_name
                    warehouse_sheets_ = warehouse_sheets_.filter(
                        invoice_line__unit_name=unit_name)
                    available = 0
                    for line in warehouse_sheets_:
                        available = line.available
                list_item['available'] = available
                availables_list.append(list_item)
        context['availables_list'] = json.dumps(availables_list)

        return render(request, TEMPLATE_ROOT+"ware-house.html", context)


class WareHousePrintViews(View):

    def get(self, request, *args, **kwargs):
        context = getContext(request=request)
        context['no_footer'] = True
        context['no_nav_bar'] = True
        ware_house = WareHouseRepo(request=request).ware_house(*args, **kwargs)
        context['ware_house'] = ware_house

        warehouse_sheets = WareHouseSheetRepo(request=request).list(
            ware_house_id=ware_house.id).order_by('date_registered')

        products = ProductRepo(request=request).list()
        availables_list = []
        for product in products:
            line = warehouse_sheets.filter(product_id=product.id).filter(
                ware_house=ware_house).first()
            if line is not None:
                list_item = {'product': {'id': product.pk, 'title': product.title,
                                         'get_absolute_url': product.get_absolute_url()}}
                list_item['available'] = line.available()
                list_item['unit_name'] = line.unit_name
                availables_list.append(list_item)
        context['availables_list'] = json.dumps(availables_list)

        return render(request, TEMPLATE_ROOT+"ware-house-print.html", context)


class WareHousesViews(View):
    def get(self, request, *args, **kwargs):
        context = getContext(request=request)
        ware_houses = WareHouseRepo(request=request).list(*args, **kwargs)
        context['ware_houses'] = ware_houses
        ware_houses_s = json.dumps(
            WareHouseSerializer(ware_houses, many=True).data)
        context['ware_houses_s'] = ware_houses_s

        return render(request, TEMPLATE_ROOT+"ware-houses.html", context)


class WareHouseSheetViews(View):
    def get(self, request, *args, **kwargs):
        context = getContext(request=request)
        warehouse_sheet = WareHouseSheetRepo(
            request=request).warehouse_sheet(*args, **kwargs)
        context['warehouse_sheet'] = warehouse_sheet
        warehouse_sheet_s = json.dumps(
            WareHouseSheetSerializer(warehouse_sheet).data)
        context['warehouse_sheet_s'] = warehouse_sheet_s

        ware_house_sheet_signatures = warehouse_sheet.warehousesheetsignature_set.all()
        context['ware_house_sheet_signatures'] = ware_house_sheet_signatures
        ware_house_sheet_signatures_s = json.dumps(
            WareHouseSheetSignatureSerializer(ware_house_sheet_signatures, many=True).data)
        context['ware_house_sheet_signatures_s'] = ware_house_sheet_signatures_s

        #add_signature_form
        if True:
            context['signature_statuses']=(i[0] for i in SignatureStatusEnum.choices)
            employee=EmployeeRepo(request=self.request).me
            if employee is not None:
                context['add_signature_form']=AddSignatureForm()

        return render(request, TEMPLATE_ROOT+"ware-house-sheet.html", context)
