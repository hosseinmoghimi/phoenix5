from django.contrib import admin

from .models import Page,Link,Icon,Download

# Register your models here.
admin.site.register(Page)
admin.site.register(Link)
admin.site.register(Icon)
admin.site.register(Download)