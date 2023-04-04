from django.db import models
from core.models import _,reverse,LinkHelper
from .apps import APP_NAME


class Shipper(models.Model,LinkHelper):
    region=models.ForeignKey("map.area", verbose_name=_("region"), on_delete=models.CASCADE)
    account=models.ForeignKey("accounting.account", verbose_name=_("account"), on_delete=models.CASCADE)

    class_name="shipper"
    app_name=APP_NAME
    def title(self):
        return self.account.title
    def save(self,*args, **kwargs):
        
        return super(Shipper,self).save()
    class Meta:
        verbose_name = _("Shipper")
        verbose_name_plural = _("Shippers")

    def __str__(self):
        return self.account.title
 

class Packer(models.Model,LinkHelper):
    region=models.ForeignKey("map.area", verbose_name=_("region"), on_delete=models.CASCADE)
    account=models.ForeignKey("accounting.account", verbose_name=_("account"), on_delete=models.CASCADE)

    class_name="packer"
    app_name=APP_NAME
    def title(self):
        return self.account.title
    def save(self,*args, **kwargs):
        
        return super(Packer,self).save()
    class Meta:
        verbose_name = _("Packer")
        verbose_name_plural = _("Packers")

    def __str__(self):
        return self.account.title


