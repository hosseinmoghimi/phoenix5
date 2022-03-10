from utility.calendar import PERSIAN_MONTH_NAMES, PersianCalendar
from core.middleware import get_request
from django.db import models
from core.models import Page
from django.shortcuts import reverse
from django.utils.translation import gettext as _
from .apps import APP_NAME
from utility.utils import LinkHelper
from .enums import *
from tinymce.models import HTMLField
from core.enums import ColorEnum,UnitNameEnum


class Driver(models.Model,LinkHelper):
    profile=models.ForeignKey("authentication.profile", verbose_name=_("profile"), on_delete=models.CASCADE)
    title=models.CharField(_("title"), max_length=50)
    color=models.CharField(_("color"),max_length=50,choices=ColorEnum.choices,default=ColorEnum.PRIMARY)
    class_name='driver'
    app_name=APP_NAME
    class Meta:
        verbose_name = 'Driver'
        verbose_name_plural = 'Drivers'
    def __str__(self):
        return self.profile.name


class Passenger(models.Model,LinkHelper):
    profile=models.ForeignKey("authentication.profile", verbose_name=_("profile"), on_delete=models.CASCADE)
    class_name="passenger"
    app_name=APP_NAME

    def get_trips_url(self):
        return reverse(APP_NAME+":trips",kwargs={'category_id':0,'driver_id':0,'vehicle_id':0,'passenger_id':self.pk,'trip_path_id':0})
    
    class Meta:
        verbose_name = _("Passenger")
        verbose_name_plural = _("Passengers")

    def __str__(self):
        return self.profile.name


class Area(models.Model,LinkHelper):
    code=models.CharField(_("code"), max_length=50)
    name=models.CharField(_("area"), max_length=50)
    app_name=APP_NAME
    class_name="area"
    class Meta:
        verbose_name = _("Area")
        verbose_name_plural = _("Areas")

    def __str__(self):
        return self.name



class ServiceMan(models.Model,LinkHelper):
    profile=models.ForeignKey("authentication.profile", verbose_name=_("profile"), on_delete=models.CASCADE)
    name=models.CharField(_("نام تعمیرگاه"),null=True,blank=True, max_length=50)
    address=models.CharField(_("address"),null=True,blank=True, max_length=50)
    tel=models.CharField(_("tel"),null=True,blank=True, max_length=50)
    
    app_name=APP_NAME
    class_name="serviceman"
    class Meta:
        verbose_name = _("ServiceMan")
        verbose_name_plural = _("ServiceMans")

    def __str__(self):
        return self.name if self.name is not None else self.profile.name
 