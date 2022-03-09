import profile
from django.db import models
from django.utils.translation import gettext as _
from django.shortcuts import reverse

class ShareHolder(models.Model):
    profile=models.ForeignKey("authentication.profile", verbose_name=_("profile"), on_delete=models.CASCADE)
    stock=models.IntegerField(_("میزان مشارکت"))
    account=models.ForeignKey("accounting.account", verbose_name=_("account"), on_delete=models.CASCADE)
    

    class Meta:
        verbose_name = _("ShareHolder")
        verbose_name_plural = _("ShareHolders")

    def __str__(self):
        return self.profile.name

    def get_absolute_url(self):
        return reverse("ShareHolder_detail", kwargs={"pk": self.pk})
