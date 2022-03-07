from phoenix.server_settings import ADMIN_URL,STATIC_URL,MEDIA_URL
from django.db import models
from core.models import Page,LinkHelper
from django.utils.translation import gettext as _
from django.shortcuts import reverse
from .apps import APP_NAME
from tinymce.models import HTMLField
IMAGE_FOLDER=APP_NAME+"/images/"


class Blog(Page):
 
    def save(self,*args, **kwargs):
        if self.class_name is None or self.class_name=="":
            self.class_name="blog"
        if self.app_name is None or self.app_name=="":
            self.app_name=APP_NAME
        return super(Blog,self).save(*args, **kwargs)

    class Meta:
        verbose_name = _("Blog")
        verbose_name_plural = _("Blogs")
 
 

class Carousel(models.Model):
    app_name=models.CharField(_("app_name"), max_length=50)
    image_banner = models.ImageField(_("تصویر اسلایدر  1333*2000 "), upload_to=IMAGE_FOLDER +
                                     'Banner/', height_field=None, width_field=None, max_length=None)
    title = models.CharField(_("عنوان"), null=True, blank=True, max_length=500)
    body = HTMLField(_("بدنه"), null=True, blank=True, max_length=2000)
    text_color = models.CharField(_("رنگ متن"), default="#fff", max_length=20)
    height=models.IntegerField(_("height"),default=350)
    priority = models.IntegerField(_("ترتیب"), default=100)
    archive = models.BooleanField(_("بایگانی شود؟"), default=False)
    tag_number = models.IntegerField(_("عدد برچسب"), default=100)
    links=models.ManyToManyField("core.link",blank=True, verbose_name=_("links"))
    tag_text = models.CharField(
        _("متن برچسب"), max_length=100, blank=True, null=True)
    class_name="carousel"
    class Meta:
        verbose_name = _("Carousel")
        verbose_name_plural = _("اسلایدر های صفحه اصلی")

    def image(self):
        return MEDIA_URL+str(self.image_banner)

    def __str__(self):
        return str(self.priority)

    def get_edit_btn(self):
        return f"""
        <a target="_blank" href="{self.get_edit_url()}" title="ویرایش اسلایدر">
        <i class="fa fa-edit text-info"></i>
        </a>
        """
    def get_edit_url(self):
        return f'{ADMIN_URL}{APP_NAME}/{self.class_name}/{self.pk}/change/'



class OurWork(Page):
 
    def save(self,*args, **kwargs):
        if self.class_name is None or self.class_name=="":
            self.class_name="ourwork"
        if self.app_name is None or self.app_name=="":
            self.app_name=APP_NAME
        return super(OurWork,self).save(*args, **kwargs)

    class Meta:
        verbose_name = _("OurWork")
        verbose_name_plural = _("OurWorks")
 
class Feature(Page):
 
    def save(self,*args, **kwargs):
        if self.class_name is None or self.class_name=="":
            self.class_name="feature"
        if self.app_name is None or self.app_name=="":
            self.app_name=APP_NAME
        return super(Feature,self).save(*args, **kwargs)

    class Meta:
        verbose_name = _("Feature")
        verbose_name_plural = _("Features")
 
 