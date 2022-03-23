from django.core.files.storage import FileSystemStorage
from django.db import models
from django.http import Http404
from django.shortcuts import reverse
from django.utils.translation import gettext as _
from phoenix.settings import ADMIN_URL, MEDIA_URL, STATIC_URL, UPLOAD_ROOT
from tinymce.models import HTMLField
from utility.calendar import PersianCalendar
from utility.utils import LinkHelper

from .apps import APP_NAME
from .enums import *

IMAGE_FOLDER = "images/"
upload_storage = FileSystemStorage(location=UPLOAD_ROOT, base_url='/uploads')


class ImageMixin():

    @property
    def image(self):
        if self.image_main_origin:
            return MEDIA_URL+str(self.image_main_origin)

    @property
    def thumbnail(self):
        return self.get_or_create_thumbnail()

    def get_or_create_thumbnail(self, *args, **kwargs):
        if self.thumbnail_origin:
            return MEDIA_URL+str(self.thumbnail_origin)
        try:
            if self.image_main_origin is None:
                return f'{STATIC_URL}{self.app_name}/img/pages/thumbnail/{self.class_name}.png'
        except:
            return f'{STATIC_URL}{self.app_name}/img/pages/thumbnail/{self.class_name}.png'
        # Opening the uploaded image

        from PIL import Image as PilImage
        from io import BytesIO
        import sys
        from django.core.files.uploadedfile import InMemoryUploadedFile

        image = PilImage.open(self.image_main_origin)

        width11, height11 = image.size
        ratio11 = float(height11)/float(width11)

        output = BytesIO()
        from .repo import ParameterRepo
        THUMBNAIL_DIMENSION = ParameterRepo(app_name=APP_NAME).parameter(
            name=ParameterNameEnum.THUMBNAIL_DIMENSION, default=150).value
        try:
            a = THUMBNAIL_DIMENSION+100
        except:
            THUMBNAIL_DIMENSION = 250
        # Resize/modify the image
        image = image.resize((THUMBNAIL_DIMENSION, int(
            ratio11*float(THUMBNAIL_DIMENSION))), PilImage.ANTIALIAS)

        # after modifications, save it to the output
        image.save(output, format='JPEG', quality=95)

        output.seek(0)

        # change the imagefield value to be the newley modifed image value
        image_name = f"{self.image_main_origin.name.split('.')[0]}.jpg"
        image_path = IMAGE_FOLDER+'image/jpeg'
        self.thumbnail_origin = InMemoryUploadedFile(
            output, 'ImageField', image_name, image_path, sys.getsizeof(output), None)
        return MEDIA_URL+str(self.thumbnail_origin)


class Page(models.Model, LinkHelper, ImageMixin):
    title = models.CharField(_("عنوان"), max_length=5000)
    thumbnail_origin = models.ImageField(_("تصویر کوچک"), upload_to=IMAGE_FOLDER+'ImageBase/Thumbnail/',
                                         null=True, blank=True, height_field=None, width_field=None, max_length=None)

    short_description = HTMLField(
        _("توضیحات کوتاه"), null=True, blank=True, max_length=50000)
    description = HTMLField(_("توضیحات"), null=True,
                            blank=True, max_length=50000)
    app_name = models.CharField(
        _("app_name"), null=True, blank=True, max_length=50)
    class_name = models.CharField(
        _("class_name"), null=True, blank=True, max_length=50)
    date_added = models.DateTimeField(
        _("date_added"), auto_now=False, auto_now_add=True)
    priority = models.IntegerField(_("ترتیب"), default=1000)
    archive = models.BooleanField(_("archive?"), default=False)

    def likes_count(self):
        return 0

    def class_title(self):
        class_title = ""
        if self.class_name == "product":
            class_title = "کالا"
        if self.class_name == "project":
            class_title = "پروژه"
        if self.class_name == "service":
            class_title = "سرویس"
        if self.class_name == "organizationunit":
            class_title = "واحد سازمانی"
        return class_title

    @property
    def full_title(self):
        try:
            if self.parent is None:
                return self.title
            return self.parent.full_title+" : "+self.title
        except:
            return self.title
    def get_breadcrumb_link(self):
        aaa=f"""
                    <li class="breadcrumb-item"><a href="{self.get_absolute_url()}">
                    <span class="farsi">
                    {self.title}
                    </span>
                    </a></li> 
                    
                    
                    """
        if self.parent is None:
            return aaa
        return self.parent.get_breadcrumb_link()+aaa
    def get_breadcrumb(self):
        return f"""
        
                <nav aria-label="breadcrumb">
                <ol class="breadcrumb">
                    {self.get_breadcrumb_link()}
                </ol>
                </nav>
        """
       

    class Meta:
        verbose_name = _("Page")
        verbose_name_plural = _("Pages")

    def __str__(self):
        # return f"""{self.app_name or ""} {self.class_name or ""} {self.title}"""
        return f"""{self.title}"""


class PageComment(models.Model):
    profile=models.ForeignKey("authentication.profile", verbose_name=_("profile"), on_delete=models.CASCADE)
    page=models.ForeignKey("page", verbose_name=_("page"), on_delete=models.CASCADE)
    comment=HTMLField(verbose_name="comment")
    date_added=models.DateTimeField(_("date_added"), auto_now=False, auto_now_add=True)
    def persian_date_added(self):
        return PersianCalendar().from_gregorian(self.date_added)
    
    class Meta:
        verbose_name = _("PageComment")
        verbose_name_plural = _("PageComments")


class Icon(models.Model):
    title = models.CharField(_("title"), null=True, blank=True, max_length=50)
    icon_fa = models.CharField(
        _("icon fa"), null=True, blank=True, max_length=50)
    icon_material = models.CharField(
        _("material_icon"), null=True, blank=True, max_length=50)
    icon_svg = models.TextField(_("svg_icon"), null=True, blank=True)
    profile = models.ForeignKey("authentication.profile", null=True,
                                blank=True, verbose_name=_("profile"), on_delete=models.CASCADE)
    color = models.CharField(
        _("color"), choices=ColorEnum.choices, default=ColorEnum.PRIMARY, max_length=50)
    width = models.IntegerField(_("عرض آیکون"), null=True, blank=True)
    height = models.IntegerField(_("ارتفاع آیکون"), null=True, blank=True)
    priority = models.IntegerField(_("priority"), default=1000)
    image_origin = models.ImageField(_("تصویر آیکون"), upload_to=IMAGE_FOLDER+'Icon/',
                                     height_field=None, null=True, blank=True, width_field=None, max_length=None)

    def get_icon_tag(self, icon_style='', color=None, no_color=False):

        if color is not None:
            self.color = color
        text_color = ''
        if not no_color and self.color is not None:
            text_color = 'text-'+self.color

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

    def get_icon_tag_pure(self, icon_style='', color=None, no_color=False):

        if color is not None:
            self.color = color
        text_color = ''
        if not no_color and self.color is not None:
            text_color = 'text-'+self.color

        if self.image_origin is not None and self.image_origin:
            return f'<img src="{MEDIA_URL}{str(self.image_origin)}" alt="{self.title}" height="{self.height}" width="{self.width}">'

        if self.icon_material is not None and len(self.icon_material) > 0:
            return f'<i style="{icon_style}" class="material-icons">{self.icon_material}</i>'

        if self.icon_fa is not None and len(self.icon_fa) > 0:
            return f'<i style="{icon_style}" class="{self.icon_fa}"></i>'

        if self.icon_svg is not None and len(self.icon_svg) > 0:
            return f'<span  style="{icon_style}" class="{text_color}">{self.icon_svg}</span>'
        return ''

    class Meta:
        verbose_name = _("Icon")
        verbose_name_plural = _("Icons")

    def __str__(self):
        return self.title


class Download(Icon):
    file = models.FileField(_("فایل ضمیمه"), null=True, blank=True,
                            upload_to=APP_NAME+'/downloads', storage=upload_storage, max_length=100)
    mirror_link = models.CharField(
        _('آدرس بیرونی'), null=True, blank=True, max_length=10000)
    date_added = models.DateTimeField(
        _("افزوده شده در"), auto_now=False, auto_now_add=True)
    date_updated = models.DateTimeField(
        _("اصلاح شده در"), auto_now_add=False, auto_now=True)
    download_counter = models.IntegerField(_("download_counter"), default=0)
    profiles = models.ManyToManyField(
        "authentication.profile", blank=True, related_name="profile_downloads", verbose_name=_("profiles"))
    is_open = models.BooleanField(_("is_open?"), default=False)

    def get_download_url(self):
        if self.mirror_link and self.mirror_link is not None:
            return self.mirror_link
        if self.file:
            return reverse(APP_NAME+':download', kwargs={'pk': self.pk})
        else:
            return ''

    def download_response(self):
        #STATIC_ROOT2 = os.path.join(BASE_DIR, STATIC_ROOT)
        file_path = str(self.file.path)
        # return JsonResponse({'download:':str(file_path)})
        import os
        from django.http import HttpResponse
        if os.path.exists(file_path):
            with open(file_path, 'rb') as fh:
                response = HttpResponse(
                    fh.read(), content_type="application/force-download")
                response['Content-Disposition'] = 'inline; filename=' + \
                    os.path.basename(file_path)
                self.download_counter += 1
                self.save()
                return response
        from log.repo import LogRepo
        LogRepo().add_log(title="Http404 core models", app_name=APP_NAME)
        raise Http404

    class Meta:
        verbose_name = _("Download")
        verbose_name_plural = _("Downloads")

    def __str__(self):
        return self.title


class Link(Icon):
    url = models.CharField(_("url"), max_length=2000)
    new_tab=models.BooleanField(_("new_tab"),default=False)
    class Meta:
        verbose_name = _("Link")
        verbose_name_plural = _("Links")

    def get_absolute_url(self):
        return reverse("Link_detail", kwargs={"pk": self.pk})

    def get_link_btn(self):
        target='target="_blank"' if self.new_tab else ''
        return f"""

            <a {target} class="btn btn-{self.color} " href="{self.url}">
            <span class="ml-2">
            {self.get_icon_tag_pure()}
            </span>
            {self.title}
            </a>
        """

class PageLink(Link, LinkHelper):
    page = models.ForeignKey("page", verbose_name=_(
        "page"), on_delete=models.CASCADE)
    class_name = "pagelink"
    app_name = APP_NAME

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'PageLink'
        verbose_name_plural = 'PageLinks'


class PageDownload(Download, LinkHelper):
    page = models.ForeignKey("page", verbose_name=_(
        "page"), on_delete=models.CASCADE)
    class_name = "pagedownload"
    app_name = APP_NAME

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'PageDownload'
        verbose_name_plural = 'PageDownloads'


class PageLike(models.Model):
    page = models.ForeignKey("page", verbose_name=_(
        "page"), on_delete=models.CASCADE)
    profile = models.ForeignKey("authentication.profile", verbose_name=_(
        "profile"), on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'PageLike'
        verbose_name_plural = 'PageLikes'

    def __str__(self):
        return self.page.title+" "+self.profile.name


class Parameter(models.Model):
    app_name = models.CharField(_("app_name"), max_length=50)
    name = models.CharField(_("app_name"), max_length=50)
    origin_value = models.CharField(
        _("origin_value"), null=True, blank=True, max_length=50000)
    class_name = "parameter"

    @property
    def value(self):
        if self.origin_value is None:
            return ''
        return self.origin_value

    @property
    def boolean_value(self):
        if self.origin_value is None:
            return False
        if self.origin_value == 'True':
            return True
        if self.origin_value == '1':
            return True
        if self.origin_value == 'true':
            return True
        if self.origin_value == 'بله':
            return True
        if self.origin_value == 'درست':
            return True
        if self.origin_value == 'آری':
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


class Image(models.Model, LinkHelper):
    app_name=APP_NAME
    class_name='image'

    title = models.CharField(_("title"), max_length=50)
    description = HTMLField(_("توضیحات"), null=True,
                            blank=True, max_length=50000)

    thumbnail_origin = models.ImageField(_("تصویر کوچک"), upload_to=IMAGE_FOLDER+'ImageBase/Thumbnail/',
                                         null=True, blank=True, height_field=None, width_field=None, max_length=None)
    image_main_origin = models.ImageField(_("تصویر اصلی"), null=True, blank=True, upload_to=IMAGE_FOLDER +
                                          'ImageBase/Main/', height_field=None, width_field=None, max_length=None)
    image_header_origin = models.ImageField(_("تصویر سربرگ"), null=True, blank=True, upload_to=IMAGE_FOLDER +
                                            'ImageBase/Header/', height_field=None, width_field=None, max_length=None)
    def __str__(self):
        return self.title
    class Meta:
        verbose_name = _("Image")
        verbose_name_plural = _("تصاویر")

    @property
    def image(self):
        if self.image_main_origin:
            return MEDIA_URL+str(self.image_main_origin)

    @property
    def thumbnail(self):
        return self.get_or_create_thumbnail()

    def get_or_create_thumbnail(self, *args, **kwargs):
        if self.thumbnail_origin:
            return MEDIA_URL+str(self.thumbnail_origin)
        try:
            if self.image_main_origin is None:
                return f'{STATIC_URL}{self.app_name}/img/pages/thumbnail/{self.class_name}.png'
        except:
            return f'{STATIC_URL}{self.app_name}/img/pages/thumbnail/{self.class_name}.png'
        # Opening the uploaded image

        from PIL import Image as PilImage
        from io import BytesIO
        import sys
        from django.core.files.uploadedfile import InMemoryUploadedFile

        image = PilImage.open(self.image_main_origin)

        width11, height11 = image.size
        ratio11 = float(height11)/float(width11)
     

        output = BytesIO()
        from .repo import ParameterRepo
        THUMBNAIL_DIMENSION = int(ParameterRepo(app_name=APP_NAME).parameter(
            name=ParameterNameEnum.THUMBNAIL_DIMENSION, default=150).value)
         
        # try:
        #     a = THUMBNAIL_DIMENSION+100
        # except:
        #     THUMBNAIL_DIMENSION = 250
        # Resize/modify the image
        image = image.resize((THUMBNAIL_DIMENSION, int(ratio11*float(THUMBNAIL_DIMENSION))), PilImage.ANTIALIAS)
        
        # after modifications, save it to the output
        image.save(output, format='JPEG', quality=95)
   

        output.seek(0)

        # change the imagefield value to be the newley modifed image value
        image_name = f"{self.image_main_origin.name.split('.')[0]}.jpg"
        image_path = IMAGE_FOLDER+'ImageBase/Thumbnail'
        self.thumbnail_origin = InMemoryUploadedFile(output, 'ImageField', image_name, image_path, sys.getsizeof(output), None)
       
        self.save()
        # return MEDIA_URL+str(self.image_main_origin)
        return MEDIA_URL+str(self.thumbnail_origin)


class PageImage(Image,LinkHelper):
    page=models.ForeignKey("page", verbose_name=_("page"), on_delete=models.CASCADE)
    app_name=APP_NAME
    class_name='pageimage'

    class Meta:
        verbose_name = _("PageImage")
        verbose_name_plural = _("PageImages")
 

class Picture(models.Model, LinkHelper):
    app_name = models.CharField(_("app_name"), max_length=50)
    name = models.CharField(_("name"), max_length=50)
    image_origin = models.ImageField(_("image"), upload_to=IMAGE_FOLDER+"pictures/",
                                     null=True, blank=True, height_field=None, width_field=None, max_length=None)
    class_name = "picture"

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
