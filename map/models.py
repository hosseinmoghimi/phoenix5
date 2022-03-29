from django.db import models
from django.db.models import Sum
from django.shortcuts import reverse

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
 


class PageLocation(models.Model):
    page=models.ForeignKey("core.page", verbose_name=_("page"), on_delete=models.CASCADE)
    location=models.ForeignKey("location", verbose_name=_("location"), on_delete=models.CASCADE)
    date_added=models.DateTimeField(_("date_added"), auto_now=False, auto_now_add=True)

    class Meta:
        verbose_name = _("PageLocation")
        verbose_name_plural = _("PageLocations")

    def __str__(self):
        return f"""{self.page.title} - {self.location.title}"""
 