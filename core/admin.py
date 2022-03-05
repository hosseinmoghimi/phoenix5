from django.contrib import admin

from .models import Page,Link,Icon,Download, Parameter, Picture

# Register your models here.
admin.site.register(Page)
admin.site.register(Link)
admin.site.register(Icon)
admin.site.register(Download)
admin.site.register(Picture)
admin.site.register(Parameter)