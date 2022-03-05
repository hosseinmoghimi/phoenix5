from django.db import models
from accounting.models import Invoice,Product as AccountingProduct
from django.utils.translation import gettext as _
from django.shortcuts import reverse
from .apps import APP_NAME
# Create your models here.


class Order(Invoice):

    

    class Meta:
        verbose_name = _("Order")
        verbose_name_plural = _("Orders")
 

    def get_absolute_url(self):
        return reverse("Order_detail", kwargs={"pk": self.pk})


    def save(self,*args, **kwargs):
        self.class_name="order"
        self.app_name=APP_NAME
        return super(Order,self).save(*args, **kwargs)



class Product(AccountingProduct):

    

    class Meta:
        verbose_name = _("Product")
        verbose_name_plural = _("Products")
 
    def save(self,*args, **kwargs):
        
        if self.class_name is None or self.class_name=="":
            self.class_name="product"
        if self.app_name is None or self.app_name=="":
            self.app_name=APP_NAME
        return super(Product,self).save(*args, **kwargs)