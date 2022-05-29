from django.db import models
from core.models import _,reverse,Page
from accounting.models import Asset
from realestate.apps import APP_NAME
from realestate.enums import *

class Property(Asset):
    agent=models.ForeignKey("accounting.account", verbose_name=_("مسئول فروش"),null=True,blank=True, on_delete=models.SET_NULL)
    floor=models.CharField(_("طبقه"),max_length=50,choices=FloorEnum.choices,default=FloorEnum.HAMKAF)
    garage=models.IntegerField(_("تعداد گاراژ"),default=0)
    elevator=models.BooleanField(_("آسانسور دارد؟"),default=False)
    bed_rooms=models.IntegerField(_("تعداد خواب"),default=1)
    bath_rooms=models.IntegerField(_("تعداد سرویس بهداشتی"),default=1)
    kitchen_type=models.CharField(_("نوع آشپزخانه"),choices=KitchenTypeEnum.choices,default=KitchenTypeEnum.REGULAR, max_length=50)
    area=models.IntegerField(_("مساحت"))
    address=models.CharField(_("آدرس"),null=True,blank=True, max_length=500)

    def save(self,*args, **kwargs):
        if self.class_name is None or self.class_name == "":
            self.class_name = "property"
        if self.app_name is None or self.app_name == "":
            self.app_name = APP_NAME
        return super(Property,self).save(*args, **kwargs)
    

    class Meta:
        verbose_name = _("Property")
        verbose_name_plural = _("Propertys")
 