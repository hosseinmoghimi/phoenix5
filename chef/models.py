from django.db import models
from accounting.models import Invoice,Product as AccountingProduct
from django.utils.translation import gettext as _
from django.shortcuts import reverse
from chef.apps import APP_NAME
from core.models import Page
# Create your models here.

 

class Food(Page):

    class Meta:
        verbose_name = _("Food")
        verbose_name_plural = _("Food")
 
    def save(self,*args, **kwargs):
        if self.class_name is None or self.class_name=="":
            self.class_name="food"
        if self.app_name is None or self.app_name=="":
            self.app_name=APP_NAME
        return super(Food,self).save(*args, **kwargs)