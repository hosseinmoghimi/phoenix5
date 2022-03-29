from xmlrpc.client import boolean
from core.enums import ColorEnum
from phoenix.server_settings import ADMIN_URL,STATIC_URL,MEDIA_URL
from django.db import models
from core.models import Page,LinkHelper
from django.utils.translation import gettext as _
from django.shortcuts import reverse
from .apps import APP_NAME
from tinymce.models import HTMLField
IMAGE_FOLDER=APP_NAME+"/images/"


class Blog(Page):
    for_home=models.BooleanField(_("for_home"),default=False)
 
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
    for_home=models.BooleanField(_("for_home"),default=False)
 
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
    for_home=models.BooleanField(_("for_home"),default=False)
 
    def save(self,*args, **kwargs):
        if self.class_name is None or self.class_name=="":
            self.class_name="feature"
        if self.app_name is None or self.app_name=="":
            self.app_name=APP_NAME
        return super(Feature,self).save(*args, **kwargs)

    class Meta:
        verbose_name = _("Feature")
        verbose_name_plural = _("Features")
  

class Testimonial(models.Model):
    for_home = models.BooleanField(_("نمایش در صفحه خانه"), default=False)
    title = models.CharField(_("عنوان"),null=True,blank=True, max_length=2000)
    body = HTMLField(_("متن"), max_length=20000, null=True, blank=True)
    footer = models.CharField(_("پانوشت"), max_length=200)
    priority = models.IntegerField(_("ترتیب"), default=100)
    profile = models.ForeignKey("authentication.Profile", null=True,
                                blank=True, verbose_name=_("profile"), on_delete=models.PROTECT)
    class_name="testimonial"
    class Meta:
        verbose_name = _("Testimonial")
        verbose_name_plural = _("گفته های مشتریان")
    def image(self):
        if self.image_origin:
            return MEDIA_URL+str(self.image_origin)
        return STATIC_URL+"web/testimonial/icon.png"
    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("Testimonial_detail", kwargs={"pk": self.pk})

    def get_edit_url(self):
        return f'{ADMIN_URL}{APP_NAME}/{self.class_name}/{self.pk}/change/'


class CountDownItem(models.Model):
    title = models.CharField(_("Title"), max_length=500, blank=True, null=True)
    pretitle = models.CharField(
        _("Pre Title"), max_length=500, blank=True, null=True)
    for_home = models.BooleanField(_("نمایش در صفحه اصلی"), default=False)
    image_origin = models.ImageField(_("تصویر"), upload_to=IMAGE_FOLDER+'CountDownItem/',
                                     null=True, blank=True, height_field=None, width_field=None, max_length=None)
    counter = models.IntegerField(_("شمارنده"), default=100)
    priority = models.IntegerField(_("ترتیب"), default=100)

    class Meta:
        verbose_name = _("CountDownItem")
        verbose_name_plural = _("شمارنده ها")

    def image(self):
        if self.image_origin:
            return MEDIA_URL+str(self.image_origin)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return self.title

    def get_edit_url(self):
        return f'{ADMIN_URL}{APP_NAME}/coundownitem/{self.pk}/change/'


class OurTeam(models.Model):
    for_home=models.BooleanField(_("for_home"),default=False)
    class_name="ourteam"
    app_name=APP_NAME
    app_name=models.CharField(_("app_name"),null=True,blank=True, max_length=50)
    profile = models.ForeignKey("authentication.Profile", verbose_name=_(
        "پروفایل"), on_delete=models.CASCADE)
    job = models.CharField(_("سمت"), max_length=100)
    description = HTMLField(_("توضیحات"),null=True,blank=True, max_length=50000)
    priority = models.IntegerField(_("ترتیب"), default=1000)
    links = models.ManyToManyField(
        "core.link", verbose_name=_("links"), blank=True)
    
    for_home=models.BooleanField(_("for_home"),default=False)
    def __str__(self):
        return self.profile.name

    def __unicode__(self):
        return self.name

    def blogs(self):
        return Blog.objects.filter(author=self)
    class Meta:
        db_table = 'OurTeam'
        managed = True
        verbose_name = 'OurTeam'
        verbose_name_plural = 'تیم ما'

    def get_absolute_url(self):
        return reverse(APP_NAME+":ourteam",kwargs={'pk':self.pk})

    def social_links(self):
        return self.links.order_by('priority')
    def get_edit_url(self):
        return f"{ADMIN_URL}{APP_NAME}/{self.class_name}/{self.pk}/change/"


class Technology(Page):
    # question = models.CharField(_("سوال"), max_length=200)  

    def save(self):
        self.child_class_title='تکنولوژی'
        self.class_name = 'technology'
        self.app_name = APP_NAME
        super(Technology, self).save()

    class Meta:
        verbose_name = _("Technology")
        verbose_name_plural = _("تکنولوژی")


class FAQ(models.Model):
    for_home = models.BooleanField(_("نمایش در صفحه خانه"), default=False)
    color = models.CharField(
        _("رنگ"), choices=ColorEnum.choices, default=ColorEnum.PRIMARY, max_length=50)

    # icon = models.ForeignKey(
    #     "core.icon", null=True, blank=True, on_delete=models.SET_NULL)
    priority = models.IntegerField(_("ترتیب"))
    question = models.CharField(_("سوال"), max_length=200)
    answer = models.CharField(_("پاسخ"), max_length=5000)
    class_name='faq'

    class Meta:
        verbose_name = _("FAQ")
        verbose_name_plural = _("پرسش های متداول")

    def __str__(self):
        return self.question

    def get_edit_url(self):
        return f'{ADMIN_URL}{APP_NAME}/{self.class_name}/{self.pk}/change/'

    def get_absolute_url(self):
        return reverse("web:faq")

