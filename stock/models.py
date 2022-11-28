import profile
from django.db import models
from core.models import LinkHelper
from django.utils.translation import gettext as _
from django.shortcuts import reverse
from stock.apps import APP_NAME

class ShareHolder(models.Model,LinkHelper):
    # account=models.ForeignKey("accounting.account", verbose_name=_("account"), on_delete=models.CASCADE)
    account=models.ForeignKey("accounting.account", verbose_name=_("account"), on_delete=models.CASCADE)
    asset=models.ForeignKey("accounting.asset", verbose_name=_("asset"), on_delete=models.CASCADE)
    stock=models.IntegerField(_("میزان مشارکت"))
    class_name="shareholder"
    app_name=APP_NAME

    class Meta:
        verbose_name = _("ShareHolder")
        verbose_name_plural = _("ShareHolders")

    def __str__(self):
        return self.account.title
 