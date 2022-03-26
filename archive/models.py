from django.db import models
from django.forms import CharField
from django.utils.translation import gettext as _
from core.models import LinkHelper
from .apps import APP_NAME
from django.shortcuts import reverse


# Create your models here.
class Folder(models.Model,LinkHelper):
    name=models.CharField(_("name"), max_length=100)
    parent=models.ForeignKey("folder",related_name="childs",null=True,blank=True, verbose_name=_("parent"), on_delete=models.CASCADE)
    class_name='folder'
    app_name=APP_NAME
    class Meta:
        verbose_name = _("Folder")
        verbose_name_plural = _("Folders")

    def __str__(self):
        return self.name
    def save(self,*args, **kwargs):
        return super(Folder,self).save()

    def get_breadcrumb_link(self):
        aaa=f"""
                    <li class="breadcrumb-item"><a href="{self.get_absolute_url()}">
                    <span class="farsi">
                    {self.name}
                    </span>
                    </a></li> 
                    
                    
                    """
        if self.parent is None:
            return aaa
        return self.parent.get_breadcrumb_link()+aaa
    def get_breadcrumb(self):
        return f"""
        
                <nav aria-label="breadcrumb">
                <ol class="breadcrumb">
                    {self.get_breadcrumb_link()}
                </ol>
                </nav>
        """
     