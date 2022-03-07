from django.core.files.storage import FileSystemStorage
from django.db import models
from django.shortcuts import reverse
from django.utils.translation import gettext as _
from phoenix.settings import ADMIN_URL, MEDIA_URL, STATIC_URL, UPLOAD_ROOT
from tinymce.models import HTMLField
from utility.calendar import PersianCalendar
from utility.utils import LinkHelper

from .apps import APP_NAME
from .enums import *

IMAGE_FOLDER="images"
upload_storage = FileSystemStorage(location=UPLOAD_ROOT, base_url='/uploads')


class Page(models.Model,LinkHelper):
    title=models.CharField(_("عنوان"), max_length=5000)
    short_description=HTMLField(_("توضیحات کوتاه"),null=True,blank=True, max_length=50000)
    description=HTMLField(_("توضیحات"),null=True,blank=True, max_length=50000)
    app_name=models.CharField(_("app_name"),null=True,blank=True, max_length=50)
    class_name=models.CharField(_("class_name"),null=True,blank=True, max_length=50)
    date_added=models.DateTimeField(_("date_added"), auto_now=False, auto_now_add=True)
    priority=models.IntegerField(_("ترتیب"),default=1000)
    @property
    def thumbnail(self):
        return ""

    class Meta:
        verbose_name = _("Page")
        verbose_name_plural = _("Pages")

    def __str__(self):
        # return f"""{self.app_name or ""} {self.class_name or ""} {self.title}"""
        return f"""{self.title}"""
 

class Download(models.Model):
    name=models.CharField(_("name"), max_length=50)

    

    class Meta:
        verbose_name = _("Download")
        verbose_name_plural = _("Downloads")

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("Download_detail", kwargs={"pk": self.pk})


class Icon(models.Model):
    name=models.CharField(_("name"), null=True,blank=True,max_length=50)
    icon_fa=models.CharField(_("fa"), null=True,blank=True,max_length=50)
    icon_material=models.CharField(_("material_icon"),null=True,blank=True, max_length=50)
    icon_svg=models.TextField(_("svg_icon"),null=True,blank=True)
    color=models.CharField(_("color"),choices=ColorEnum.choices,default=ColorEnum.PRIMARY, max_length=50)
    width = models.IntegerField(_("عرض آیکون"), null=True, blank=True)
    height = models.IntegerField(_("ارتفاع آیکون"), null=True, blank=True)
    image_origin = models.ImageField(_("تصویر آیکون"), upload_to=IMAGE_FOLDER+'Icon/',
                                     height_field=None, null=True, blank=True, width_field=None, max_length=None)
    
    def get_icon_tag(self, icon_style='', color=None,no_color=False):
        
        if color is not None:
            self.color = color
        text_color=''
        if not no_color and self.color is not None:
            text_color='text-'+self.color

        if self.image_origin is not None and self.image_origin:
            return f'<img src="{MEDIA_URL}{str(self.image_origin)}" alt="{self.title}" height="{self.height}" width="{self.width}">'

        if self.icon_material is not None and len(self.icon_material) > 0:
            return f'<i style="{icon_style}" class="{text_color} material-icons">{self.icon_material}</i>'

        if self.icon_fa is not None and len(self.icon_fa) > 0:
            return f'<i style="{icon_style}" class="{text_color} {self.icon_fa}"></i>'

        if self.icon_svg is not None and len(self.icon_svg) > 0:
            return f'{self.icon_svg}'
        if self.icon_svg is not None and len(self.icon_svg) > 0:
            return f'<span  style="{icon_style}" class="{text_color}">{self.icon_svg}</span>'
        return ''

    def get_icon_tag_pure(self, icon_style='', color=None,no_color=False):
        
        if color is not None:
            self.color = color
        text_color=''
        if not no_color and self.color is not None:
            text_color='text-'+self.color

        if self.image_origin is not None and self.image_origin:
            return f'<img src="{MEDIA_URL}{str(self.image_origin)}" alt="{self.title}" height="{self.height}" width="{self.width}">'

        if self.icon_material is not None and len(self.icon_material) > 0:
            return f'<i style="{icon_style}" class="{text_color} material-icons">{self.icon_material}</i>'

        if self.icon_fa is not None and len(self.icon_fa) > 0:
            return f'<i style="{icon_style}" class="{text_color} {self.icon_fa}"></i>'

        if self.icon_svg is not None and len(self.icon_svg) > 0:
            return f'<span  style="{icon_style}" class="{text_color}">{self.icon_svg}</span>'
        return ''


    class Meta:
        verbose_name = _("Icon")
        verbose_name_plural = _("Icons")

    def __str__(self):
        return self.name
 

class Link(Icon):
    url=models.CharField(_("url"), max_length=2000)
    

    class Meta:
        verbose_name = _("Link")
        verbose_name_plural = _("Links")

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("Link_detail", kwargs={"pk": self.pk})


class Parameter(models.Model):
    app_name=models.CharField(_("app_name"), max_length=50)
    name=models.CharField(_("app_name"), max_length=50)
    origin_value=models.CharField(_("origin_value"),null=True,blank=True, max_length=50000)
    class_name="parameter"

    @property
    def value(self):
        if self.origin_value is None:
            return ''
        return self.origin_value
    @property
    def boolean_value(self):
        if self.origin_value is None:
            return False
        if self.origin_value =='True':
            return True
        if self.origin_value =='1':
            return True
        if self.origin_value =='true':
            return True
        if self.origin_value =='بله':
            return True
        if self.origin_value =='درست':
            return True
        if self.origin_value =='آری':
            return True
        return False

    class Meta:
        verbose_name = _("Parameter")
        verbose_name_plural = _("Parameters")

    def __str__(self):
        return self.app_name+":"+self.name
 

    
    def get_edit_url(self):
        return f"{ADMIN_URL}{APP_NAME}/parameter/{self.pk}/change/"

    
    def get_delete_url(self):
        return f"{ADMIN_URL}{APP_NAME}/parameter/{self.pk}/delete/"


class Picture(models.Model,LinkHelper):
    app_name=models.CharField(_("app_name"), max_length=50)
    name=models.CharField(_("name"), max_length=50)
    image_origin=models.ImageField(_("image"), upload_to=IMAGE_FOLDER+"pictures/",null=True,blank=True, height_field=None, width_field=None, max_length=None)
    class_name="picture"
      
    @property
    def image(self):
        if self.image_origin and self.image_origin is not None:
            return f'{MEDIA_URL}{str(self.image_origin)}'
        return None

    class Meta:
        verbose_name = _("Picture")
        verbose_name_plural = _("Pictures")

    def __str__(self):
        return self.app_name+" : "+self.name
 
    
    def get_edit_url(self):
        return f"{ADMIN_URL}{APP_NAME}/picture/{self.pk}/change/"