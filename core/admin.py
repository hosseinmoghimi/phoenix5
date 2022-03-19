from django.contrib import admin

from .models import Image, Page,Link,Icon,Download, PageImage, PageLike, PageLink, Parameter, Picture,PageDownload

# Register your models here.
admin.site.register(Download)
admin.site.register(Image)
admin.site.register(Icon)
admin.site.register(Link)
admin.site.register(Parameter)
admin.site.register(PageLike)
admin.site.register(PageImage)
admin.site.register(Page)
admin.site.register(PageLink)
admin.site.register(PageDownload)
admin.site.register(Picture)