from django.contrib import admin

from web.models import FAQ, Blog, Carousel, CountDownItem, Feature, OurTeam, OurWork, Technology, Testimonial

# Register your models here.
admin.site.register(Blog)
admin.site.register(Feature)
admin.site.register(OurWork)
admin.site.register(Carousel)
admin.site.register(Testimonial)
admin.site.register(CountDownItem)
admin.site.register(OurTeam)
admin.site.register(Technology)
admin.site.register(FAQ)
