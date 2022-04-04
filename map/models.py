from django.db import models
from django.db.models import Sum
from django.shortcuts import reverse
from core.enums import ColorEnum

from core.settings import ADMIN_URL
from .apps import APP_NAME
from django.utils.translation import gettext as _
from .settings import *
from .enums import *
from utility.utils import LinkHelper



class Location(models.Model,LinkHelper):
    
    title = models.CharField(
        _("عنوان نقطه"), max_length=100)
    location = models.CharField(_("لوکیشن"), max_length=1000)
    latitude=models.CharField(_("latitude"),null=True,blank=True, max_length=50)
    longitude=models.CharField(_("longitude"),null=True,blank=True, max_length=50)


    creator = models.ForeignKey("authentication.profile", null=True,
                                blank=True,related_name="maplocation_set", verbose_name=_("profile"), on_delete=models.CASCADE)
    date_added = models.DateTimeField(
        _("date_added"), auto_now=False, auto_now_add=True)
    class_name = "location"
    app_name=APP_NAME
    class Meta:
        verbose_name = _("لوکیشن")
        verbose_name_plural = _("لوکیشن ها")

    def __str__(self):
        return f'{self.title}'

    
    def save(self, *args, **kwargs):
        if self.location is not None:
            self.location = self.location.replace('width="600"', 'width="100%"')
            self.location = self.location.replace('height="450"', 'height="400"')
        super(Location, self).save(*args, **kwargs)
 

 
    def get_link_to_map(self):
        return f'https://www.google.com/maps/search/?api=1&query={self.latitude},{self.longitude}'
    def get_link_to_map_tag(self):
        return f"""
            <a title="نمایش روی نقشه" target="_blank" href="{self.get_link_to_map()}">
                <span class="material-icons">
                    location_on
                    </span>
                
            </a>
        """
 
class Area(models.Model,LinkHelper):
    title=models.CharField(_("title"), max_length=50)
    code=models.CharField(_("code"), max_length=50)
    area = models.CharField(_("area"),blank=True,null=True, max_length=1000)
    color=models.CharField(_("color"),choices=ColorEnum.choices,default=ColorEnum.PRIMARY, max_length=50)
    app_name=APP_NAME
    class_name="area"
    class Meta:
        verbose_name = _("Area")
        verbose_name_plural = _("Areas")

    def __str__(self):
        return self.title


    def save(self, *args, **kwargs):
        if self.area is not None:
            self.area = self.area.replace('width="600"', 'width="100%"')
            self.area = self.area.replace('height="450"', 'height="400"')
        super(Area, self).save(*args, **kwargs)

class PageLocation(models.Model,LinkHelper):
    page=models.ForeignKey("core.page", verbose_name=_("page"), on_delete=models.CASCADE)
    location=models.ForeignKey("location", verbose_name=_("location"), on_delete=models.CASCADE)
    date_added=models.DateTimeField(_("date_added"), auto_now=False, auto_now_add=True)
    class_name = "pagelocation"
    app_name=APP_NAME
  
    class Meta:
        verbose_name = _("PageLocation")
        verbose_name_plural = _("PageLocations")

    def __str__(self):
        return f"""{self.page.title} - {self.location.title}"""
 