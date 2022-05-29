from django.db import models
from core.models import _,reverse,Page,LinkHelper
from health.apps import APP_NAME
from health.enums import *



class Drug(Page):
  
    def save(self,*args, **kwargs):
        if self.class_name is None or self.class_name == "":
            self.class_name = "drug"
        if self.app_name is None or self.app_name == "":
            self.app_name = APP_NAME
        return super(Drug,self).save(*args, **kwargs)
    

    class Meta:
        verbose_name = _("Drug")
        verbose_name_plural = _("Drugs")
 

class Patient(models.Model,LinkHelper):
    account=models.ForeignKey("accounting.account", verbose_name=_("account"), on_delete=models.CASCADE)
    class_name="patient"
    app_name=APP_NAME
    
    def __str__(self):
        return self.account.title

    class Meta:
        verbose_name = _("Patient")
        verbose_name_plural = _("Patients")
 