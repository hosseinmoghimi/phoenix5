from django.contrib import admin

from polls.models import Vote, Option, Poll

# Register your models here.
admin.site.register(Poll)
admin.site.register(Option)
admin.site.register(Vote)