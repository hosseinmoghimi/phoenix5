from django.db import models

from core.models import LinkHelper,_,reverse
from .apps import APP_NAME
from .enums import ContatctNameEnum


class ProfileContact(models.Model):

    class_name="profilecontact"
    class Meta:
        verbose_name = _("ProfileContact")
        verbose_name_plural = _("ProfileContacts")

    def __str__(self):
        return f"{str(self.profile)} : {self.name} : {self.value}"

 

class Contact(models.Model,LinkHelper):
    account=models.ForeignKey("accounting.account", verbose_name=_("account"), on_delete=models.CASCADE)
    name=models.CharField(_("name"),choices=ContatctNameEnum.choices,default=ContatctNameEnum.MOBILE, max_length=50)
    value=models.CharField(_("value"), max_length=50)
    url=models.CharField(_("url"),null=True,blank=True, max_length=5000)
    icon=models.CharField(_("icon"), null=True,blank=True, max_length=5000)
    bs_class=models.CharField(_("bootstrap class"), null=True,blank=True, max_length=50)
    priority=models.IntegerField(_("priority"),default=100)
    
    class_name="contact"
    app_name=APP_NAME
    def generate_url(self):
        if self.name==ContatctNameEnum.TEL:
            self.url="tel:"+self.value
        if self.name==ContatctNameEnum.MOBILE:
            self.url="tel:"+self.value
        if self.name==ContatctNameEnum.EMAIL:
            self.url="mailto:"+self.value
        if self.name==ContatctNameEnum.WEBSITE:
            self.url=self.value
        if self.name==ContatctNameEnum.TELEGRAM:
            self.url="tel:"+self.value
        if self.name==ContatctNameEnum.WHATSAPP:
            self.url="tel:"+self.value
    def save(self):
        if self.url is None or self.url=="":
            self.generate_url()
        super(Contact,self).save()

    class Meta:
        verbose_name = _("Contact")
        verbose_name_plural = _("Contacts")

    def __str__(self):
        return f"{self.account} {self.name}"

