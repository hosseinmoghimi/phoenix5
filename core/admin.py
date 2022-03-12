from django.contrib import admin

from .models import Image, Page,Link,Icon,Download, PageLike, PageLink, Parameter, Picture,PageDownload

# Register your models here.
admin.site.register(Page)
admin.site.register(PageLike)
admin.site.register(Link)
admin.site.register(Icon)
admin.site.register(Download)
admin.site.register(Picture)
admin.site.register(Parameter)
admin.site.register(Image)
admin.site.register(PageLink)
admin.site.register(PageDownload)