from django.contrib import admin

from web.models import Blog, Carousel, Feature, OurWork

# Register your models here.
admin.site.register(Blog)
admin.site.register(Feature)
admin.site.register(OurWork)
admin.site.register(Carousel)
