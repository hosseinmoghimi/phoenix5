import profile
from authentication.models import IMAGE_FOLDER
from phoenix.server_settings import STATIC_URL
from phoenix.settings import MEDIA_URL
from projectmanager.enums import SignatureStatusEnum, StatusColor
from utility.currency import to_price
from utility.calendar import  PersianCalendar,to_persian_datetime_tag
from core.middleware import get_request
from django.db import models
from core.models import Page
from django.shortcuts import reverse
from django.utils.translation import gettext as _
from .apps import APP_NAME
from utility.utils import LinkHelper
from warehouse.enums import *
from tinymce.models import HTMLField
from core.enums import ColorEnum,UnitNameEnum
from django.utils import timezone
 
 
class WareHouse(Page):
    # store=models.ForeignKey("store",related_name="ware_houses", verbose_name=_("store"), on_delete=models.CASCADE)
    address=models.CharField(_("address"),null=True,blank=True, max_length=50)
    tel=models.CharField(_("tel"),null=True,blank=True, max_length=50)
    account=models.ForeignKey("accounting.account", verbose_name=_("account"), on_delete=models.CASCADE)
    def get_print_url(self):
        return reverse(APP_NAME+":ware_house_print",kwargs={'pk':self.pk})

    class Meta:
        verbose_name = _("WareHouse")
        verbose_name_plural = _("WareHouses")

    def save(self,*args, **kwargs):
        self.class_name="warehouse"
        self.app_name=APP_NAME
        return super(WareHouse,self).save(*args, **kwargs)
 


class WareHouseSheet(models.Model,LinkHelper):
    date_added=models.DateTimeField(_("date_added"), auto_now=False, auto_now_add=True)
    date_registered=models.DateTimeField(_("date_registered"), auto_now=False, auto_now_add=False)
    creator=models.ForeignKey("authentication.profile", verbose_name=_("creator"), on_delete=models.CASCADE)    
    invoice_line=models.ForeignKey("accounting.invoiceline", verbose_name=_("invoice_line"), on_delete=models.CASCADE)    
    quantity=models.IntegerField(_("quantity"))
    unit_name=models.CharField(_("unit_name"),choices=UnitNameEnum.choices,default=UnitNameEnum.ADAD, max_length=50)
    direction=models.CharField(_("direction"),choices=WareHouseSheetDirectionEnum.choices, max_length=50)
    ware_house=models.ForeignKey("warehouse", verbose_name=_("ware_house"), on_delete=models.CASCADE)
    status=models.CharField(_("status"),choices=WareHouseSheetStatusEnum.choices,default=WareHouseSheetStatusEnum.INITIAL, max_length=50)
    description=HTMLField(_("description"),null=True,blank=True,max_length=50000)
    class_name="warehousesheet"
    app_name=APP_NAME
    class Meta:
        verbose_name = _("WareHouseSheet")
        verbose_name_plural = _("WareHouseSheets")
    def persian_date_registered(self):
        return PersianCalendar().from_gregorian(self.date_registered)
    @property
    def product(self):
        return self.invoice_line.product
    def save(self,*args, **kwargs):
        self.class_name="warehousesheet"
        super(WareHouseSheet,self).save(*args, **kwargs)
        if len(WareHouseSheetSignature.objects.filter(request=self))==0:
            a=WareHouseSheetSignature()
            a.request=self
            from projectmanager.models import Employee
            a.employee=Employee.objects.filter(profile=self.creator).first()
            a.save()

    @property
    def available(self):
        a=0;
        for aa in WareHouseSheet.objects.filter(status=WareHouseSheetStatusEnum.DONE).filter(ware_house=self.ware_house).filter(invoice_line__product_or_service_id=self.invoice_line.product_or_service.id):
            if aa.direction==WareHouseSheetDirectionEnum.IMPORT:
                a+=aa.quantity
            if aa.direction==WareHouseSheetDirectionEnum.EXPORT:
                a-=aa.quantity
        return a
    
    def color(self):
        color="primary"
        if self.direction==WareHouseSheetDirectionEnum.IMPORT:
            color="success"
        if self.direction==WareHouseSheetDirectionEnum.EXPORT:
            color="danger"
        return color

    def __str__(self):

        return f"{self.direction} {self.invoice_line.product_or_service.title} {self.ware_house}"


class WareHouseSheetSignature(models.Model,LinkHelper):
    request = models.ForeignKey("warehousesheet", verbose_name=_(
        "ware_house_sheet"), on_delete=models.CASCADE)
    employee = models.ForeignKey("projectmanager.employee", verbose_name=_(
        "employee"), on_delete=models.PROTECT)
    date_added = models.DateTimeField(
        _("date_added"), auto_now=False, auto_now_add=True)
    description = models.CharField(_("description"), max_length=200)
    status = models.CharField(_("status"), choices=SignatureStatusEnum.choices,
                              default=SignatureStatusEnum.REQUESTED, max_length=200)

    class_name = "warehousesheetsignature"
    app_name = APP_NAME

    class Meta:
        verbose_name = _("WareHouseSheetSignature")
        verbose_name_plural = _("WareHouseSheetSignature")

    def persian_date_added(self):
        return to_persian_datetime_tag(self.date_added)

    def get_status_color(self):
        return StatusColor(self.status)

    def get_status_tag(self):
        return f"""
            <span class="badge badge-{self.get_status_color()}">{self.status}</span>
        """

    def __str__(self):
        return f"""{self.request} : امضاءکننده" {self.employee}  " :{self.status} """
 

