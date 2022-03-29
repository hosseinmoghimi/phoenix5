from django.contrib import admin

from .models import ContactMessage,Image, NavLink, Page,Link,Icon,Download, PageComment, PageImage, PageLike, PageLink, PageTag, Parameter, Picture,PageDownload, Tag

# Register your models here.
admin.site.register(ContactMessage)
# admin.site.register(SocialLink)
admin.site.register(Tag)
admin.site.register(PageTag)
admin.site.register(NavLink)
admin.site.register(Download)
admin.site.register(Image)
admin.site.register(Icon)
admin.site.register(Link)
admin.site.register(PageComment)
admin.site.register(Parameter)
admin.site.register(PageLike)
admin.site.register(PageImage)
admin.site.register(Page)
admin.site.register(PageLink)
admin.site.register(PageDownload)
admin.site.register(Picture)