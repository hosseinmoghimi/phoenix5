from inspect import signature
from django.db.models import Q
from requests import request
from accounting.repo import AccountRepo, InvoiceRepo
from authentication.repo import ProfileRepo
from django.utils import timezone
from utility.log import leolog

from warehouse.enums import *
from utility.calendar import PersianCalendar

from warehouse.apps import APP_NAME
from warehouse.models import WareHouse, WareHouseSheet, WareHouseSheetSignature
  
now=PersianCalendar().date
       
class WareHouseRepo():
    def __init__(self, *args, **kwargs):
        self.request = None
        self.user = None
        if 'request' in kwargs:
            self.request = kwargs['request']
            self.user = self.request.user
        if 'user' in kwargs:
            self.user = kwargs['user']
        self.profile=ProfileRepo(*args, **kwargs).me
        self.objects=WareHouse.objects
        self.objects = WareHouse.objects.order_by('title')
        return
        if self.user is not None and self.user.has_perm(APP_NAME+".view_warehouse"):
            self.objects = WareHouse.objects.order_by('title')
        elif self.profile is not None:
            self.objects = WareHouse.objects.filter(account__profile=self.profile).order_by('title')
        else:
            self.objects = WareHouse.objects.filter(pk__lte=0).order_by('title')

    def list(self,*args, **kwargs):
        objects=self.objects
        return objects
    def ware_house(self, *args, **kwargs):
        if 'ware_house_id' in kwargs:
            return self.objects.filter(pk=kwargs['ware_house_id']).first()
        if 'pk' in kwargs:
            return self.objects.filter(pk=kwargs['pk']).first()
        if 'store_id' in kwargs:
            return self.objects.filter(store_id=kwargs['store_id']).first()
        if 'owner_id' in kwargs:
            return self.objects.filter(owner_id=kwargs['owner_id']).first()
        if 'id' in kwargs:
            return self.objects.filter(pk=kwargs['id']).first()

    def add_ware_house(self,*args, **kwargs):
        if not self.user.has_perm(APP_NAME+".add_warehouse"):
            return 
        from projectmanager.repo import EmployeeRepo
        # employee=EmployeeRepo(request=self.request).me
        # if employee is None:
        #     return
        ware_house=WareHouse(*args, **kwargs) 
        ware_house.account_id=AccountRepo(request=self.request).get_misc().id
        ware_house.save()
        return ware_house
class WareHouseSheetSignatureRepo():
    def __init__(self, *args, **kwargs):
        self.request = None
        self.user = None
        if 'request' in kwargs:
            self.request = kwargs['request']
            self.user = self.request.user
        if 'user' in kwargs:
            self.user = kwargs['user']
        self.profile=ProfileRepo(*args, **kwargs).me
        self.objects = WareHouseSheetSignature.objects.order_by('date_added')
        return
        if self.user is not None and self.user.has_perm(APP_NAME+".view_warehouse"):
            self.objects = WareHouse.objects.order_by('title')
        elif self.profile is not None:
            self.objects = WareHouse.objects.filter(account__profile=self.profile).order_by('title')
        else:
            self.objects = WareHouse.objects.filter(pk__lte=0).order_by('title')

    def add_signature(self,*args, **kwargs):
        if not self.user.has_perm(APP_NAME+".add_warehousesheetsignature"):
            return 
        from projectmanager.repo import EmployeeRepo
        employee=EmployeeRepo(request=self.request).me
        if employee is None:
            return
        signature=WareHouseSheetSignature()
        if 'ware_house_sheet_id' in kwargs:
            signature.request_id=kwargs['ware_house_sheet_id']
        if 'status' in kwargs:
            signature.status=kwargs['status']
        if 'description' in kwargs:
            signature.description=kwargs['description'] 
        
        signature.employee_id=employee.id
        signature.save()
        return signature
    
    def list(self,*args, **kwargs):
        objects=self.objects
        return objects
    
    def ware_house_sheet_signature(self, *args, **kwargs):
        if 'ware_house_sheet_signature_id' in kwargs:
            return self.objects.filter(pk=kwargs['ware_house_sheet_signature_id']).first()
        if 'pk' in kwargs:
            return self.objects.filter(pk=kwargs['pk']).first()
        if 'store_id' in kwargs:
            return self.objects.filter(store_id=kwargs['store_id']).first()
        if 'owner_id' in kwargs:
            return self.objects.filter(owner_id=kwargs['owner_id']).first()
        if 'id' in kwargs:
            return self.objects.filter(pk=kwargs['id']).first()
            

class WareHouseSheetRepo:
    def __init__(self, *args, **kwargs):
        self.request = None
        self.user = None
        if 'request' in kwargs:
            self.request = kwargs['request']
            self.user = self.request.user
        if 'user' in kwargs:
            self.user = kwargs['user']
        self.objects = WareHouseSheet.objects.order_by('-date_registered')
        self.profile = ProfileRepo(user=self.user).me
        if self.user.has_perm(APP_NAME+".view_warehousesheet"):
            self.objects = WareHouseSheet.objects.order_by('-date_registered')
        elif self.profile is not None:
            self.objects = WareHouseSheet.objects.filter(ware_house__account__profile_id=self.profile.id).order_by('-date_registered')
            # self.objects = WareHouseSheet.objects.filter(pk__gte=0).order_by('-date_registered')
        else:
            self.objects = WareHouseSheet.objects.filter(pk__lte=0).order_by('-date_registered')

    def list(self, *args, **kwargs):
        objects = self.objects.all()
        if 'for_home' in kwargs:
            objects = objects.filter(for_home=kwargs['for_home'])
        if 'product_id'  in kwargs and kwargs['product_id'] is not None and kwargs['product_id']>0:
            objects = objects.filter(invoice_line__product_or_service_id=kwargs['product_id'])
        if 'invoice_id'  in kwargs and kwargs['invoice_id'] is not None and kwargs['invoice_id']>0:
            objects = objects.filter(invoice_line__invoice_id=kwargs['invoice_id'])
        if 'invoice_line_id'  in kwargs and kwargs['invoice_line_id'] is not None and kwargs['invoice_line_id']>0:
            objects = objects.filter(invoice_line_id=kwargs['invoice_line_id'])
        if 'ware_house_id' in kwargs and kwargs['ware_house_id'] is not None and kwargs['ware_house_id']>0:
            objects = objects.filter(ware_house_id=kwargs['ware_house_id'])
        if 'search_for' in kwargs:
            search_for=kwargs['search_for']
            objects = objects.filter(title__contains=search_for) 
        return objects
    def add_ware_house_sheets_for_invoice(self,*args, **kwargs):
        if not self.user.has_perm(APP_NAME+".add_warehousesheet"):
            return 
        from projectmanager.repo import EmployeeRepo
        employee=EmployeeRepo(request=self.request).me
        if employee is None:
            return
            
        if 'invoice_id' in kwargs:
            invoice=InvoiceRepo(request=self.request).invoice(*args, **kwargs)
            if invoice is None:
                return
        warehouse_sheets=[]
        for invoice_line in invoice.invoice_lines():
            warehouse_sheet=WareHouseSheet()
            warehouse_sheet.invoice_line_id=invoice_line.id
            if 'status' in kwargs:
                warehouse_sheet.status=kwargs['status']
            if 'ware_house_id' in kwargs:
                warehouse_sheet.ware_house_id=kwargs['ware_house_id']
            if 'direction' in kwargs:
                warehouse_sheet.direction=kwargs['direction']
                
            if 'status' in kwargs:
                warehouse_sheet.status=kwargs['status']
            employee=EmployeeRepo(request=self.request).me
            warehouse_sheet.creator=employee.account.profile
            warehouse_sheet.date_registered=now
            warehouse_sheet.quantity=0
            warehouse_sheet.save()
            warehouse_sheet.quantity=warehouse_sheet.invoice_line.quantity
            warehouse_sheet.save()
            warehouse_sheets.append(warehouse_sheet)
        
        return warehouse_sheets
    
        
    def add_ware_house_sheet(self,*args, **kwargs):
        if not self.user.has_perm(APP_NAME+".add_warehousesheet"):
            return 
        from projectmanager.repo import EmployeeRepo
        employee=EmployeeRepo(request=self.request).me
        if employee is None:
            return
        warehouse_sheet=WareHouseSheet()
        if 'invoice_line_id' in kwargs:
            warehouse_sheet.invoice_line_id=kwargs['invoice_line_id']
        if 'status' in kwargs:
            warehouse_sheet.status=kwargs['status']
        if 'ware_house_id' in kwargs:
            warehouse_sheet.ware_house_id=kwargs['ware_house_id']
        if 'direction' in kwargs:
            warehouse_sheet.direction=kwargs['direction']
        employee=EmployeeRepo(request=self.request).me
        warehouse_sheet.creator=employee.account.profile
        warehouse_sheet.date_registered=now
        warehouse_sheet.quantity=0
        warehouse_sheet.save()
        warehouse_sheet.quantity=warehouse_sheet.invoice_line.quantity
        warehouse_sheet.save()
        
        return warehouse_sheet
    
    
    def warehouse_sheet(self, *args, **kwargs):
        if 'ware_house_sheet_id' in kwargs:
            return self.objects.filter(pk= kwargs['ware_house_sheet_id']).first()
        if 'pk' in kwargs:
            return self.objects.filter(pk= kwargs['pk']).first()
        if 'id' in kwargs:
            return self.objects.filter(pk= kwargs['id']).first()
        if 'warehouse_sheet_id' in kwargs:
            return self.objects.filter(pk= kwargs['warehouse_sheet_id']).first()
        
    def change_state(self,*args, **kwargs):
        if not self.user.has_perm(APP_NAME+".change_warehousesheet"):
            return 
        warehouse_sheet=self.warehouse_sheet(*args, **kwargs) 
        if 'status' in kwargs:
            status=kwargs['status']
            if warehouse_sheet is not None:
                warehouse_sheet.status=status
                warehouse_sheet.save()
                return warehouse_sheet
  