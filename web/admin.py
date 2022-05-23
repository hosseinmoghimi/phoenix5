from django.contrib import admin

from web.models import FAQ, Blog, PricingItemSpecification,Carousel, CountDownItem, Feature, OurTeam, OurWork, PricingItem, PricingPage, Technology, Testimonial

# Register your models here.
admin.site.register(Blog)
admin.site.register(Feature)
admin.site.register(OurWork)
admin.site.register(Carousel)
admin.site.register(Testimonial)
admin.site.register(CountDownItem)
admin.site.register(PricingPage)
admin.site.register(PricingItem)
admin.site.register(PricingItemSpecification)
admin.site.register(OurTeam)
admin.site.register(Technology)
admin.site.register(FAQ)
