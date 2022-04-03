from authentication.models import IMAGE_FOLDER
from guarantee.enums import GuaranteeStatusEnum, GuaranteeTypeEnum
from phoenix.server_settings import STATIC_URL
from phoenix.settings import MEDIA_URL
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
  

class Guarantee(models.Model,LinkHelper):
    invoice_line=models.ForeignKey("accounting.invoiceline", verbose_name=_("ردیف فاکتور"), on_delete=models.CASCADE)
    start_date=models.DateField(_("شروع گارانتی"), auto_now=False, auto_now_add=False)
    end_date=models.DateField(_("پابان گارانتی"), auto_now=False, auto_now_add=False)
    status=models.CharField(_("وضعیت"),choices=GuaranteeStatusEnum.choices,default=GuaranteeStatusEnum.VALID, max_length=50)
    type=models.CharField(_("نوع گارانتی"),choices=GuaranteeTypeEnum.choices,default=GuaranteeTypeEnum.REPAIR, max_length=50)
    serial_no=models.CharField(_("شماره سریال"), max_length=50)
    conditions=models.CharField(_("شرایط"),null=True,blank=True, max_length=5000)
    description=HTMLField(_("توضیحات"),null=True,blank=True, max_length=50000)
    class_name="guarantee"
    app_name=APP_NAME
    def persian_end_date(self):
        return PersianCalendar().from_gregorian(self.end_date)
    def persian_start_date(self):
        return PersianCalendar().from_gregorian(self.start_date)
    class Meta:
        verbose_name = _("Guarantee")
        verbose_name_plural = _("Guarantees")
            
 