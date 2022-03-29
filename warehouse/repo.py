from django.db.models import Q
from authentication.repo import ProfileRepo
from django.utils import timezone

from warehouse.enums import *
from utility.calendar import PersianCalendar

from warehouse.apps import APP_NAME
from warehouse.models import WareHouse, WareHouseSheet
   


        
class WareHouseRepo():
    def __init__(self, *args, **kwargs):
        print(kwargs['request'].user)
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
            self.objects = WareHouseSheet.objects.filter(ware_house__owner__profile=self.profile).order_by('-date_registered')
            # self.objects = WareHouseSheet.objects.filter(pk__gte=0).order_by('-date_registered')
        else:
            self.objects = WareHouseSheet.objects.filter(pk__lte=0).order_by('-date_registered')

    def list(self, *args, **kwargs):
        objects = self.objects.all()
        if 'for_home' in kwargs:
            objects = objects.filter(for_home=kwargs['for_home'])
        if 'product_id' in kwargs:
            objects = objects.filter(product_id=kwargs['product_id'])
        if 'invoice_id' in kwargs:
            objects = objects.filter(invoice_id=kwargs['invoice_id'])
        if 'ware_house_id' in kwargs:
            objects = objects.filter(ware_house_id=kwargs['ware_house_id'])
        if 'search_for' in kwargs:
            search_for=kwargs['search_for']
            objects = objects.filter(title__contains=search_for) 
        return objects

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
  