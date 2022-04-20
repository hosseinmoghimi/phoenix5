from django.db import models
from bms.apps import APP_NAME
from core.enums import ColorEnum
from core.models import _,LinkHelper

class Feeder(models.Model,LinkHelper):
    name=models.CharField(_("name"), max_length=50)
    app_name=APP_NAME
    class_name="feeder"
    @property
    def relays(self):
        return self.relay_set.all()
    class Meta:
        verbose_name = _("Feeder")
        verbose_name_plural = _("Feeders")

    def __str__(self):
        return self.name 


class Scenario(models.Model,LinkHelper):
    name=models.CharField(_("name"), max_length=50)
    app_name=APP_NAME
    class_name="scenario"

    class Meta:
        verbose_name = _("Scenario")
        verbose_name_plural = _("Scenario")

    def __str__(self):
        return self.name 



class Relay(models.Model,LinkHelper):
    name=models.CharField(_("name"), max_length=50)
    feeder=models.ForeignKey("feeder", verbose_name=_("feeder"), on_delete=models.CASCADE)
    app_name=APP_NAME
    class_name="relay"
    
    @property
    def commands(self):
        return self.command_set.all()

    class Meta:
        verbose_name = _("Relay")
        verbose_name_plural = _("Relay")

    def __str__(self):
        return self.name
    
class Command(models.Model,LinkHelper):
    name=models.CharField(_("name"), max_length=50)
    relay=models.ForeignKey("relay", verbose_name=_("relay"), on_delete=models.CASCADE)
    value=models.CharField(_("value"), max_length=50)
    color=models.CharField(_("color"),choices=ColorEnum.choices,default=ColorEnum.PRIMARY, max_length=50)
    
    app_name=APP_NAME
    class_name="command"

    class Meta:
        verbose_name = _("Command")
        verbose_name_plural = _("Commands")

    def __str__(self):
        return self.name
 
