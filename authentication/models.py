from datetime import datetime
from phoenix.settings import ADMIN_URL, MEDIA_URL, STATIC_URL
from django.db import models

from .enums import ProfileStatusEnum
from django.shortcuts import reverse
from django.utils.translation import gettext as _
from django.conf import settings
from .apps import APP_NAME
IMAGE_FOLDER=APP_NAME+"/images/"
CREATE_PROFILE_ON_USER_ADD=True

if CREATE_PROFILE_ON_USER_ADD:
    from django.db.models.signals import post_save

    def create_profile_receiver(sender,instance,created,*args, **kwargs):  
        if created:
            profile=Profile(user_id=instance.id)
            profile.save()

    def save_profile_receiver(sender,instance,*args, **kwargs):    
        profile=instance.profile
        profile.save()
        # if profile.region is None:
        #     try:
        #         from core.models import Region
        #         profile.region=Region.objects.first()
        #         profile.save()
        #     except:
        #         pass
        try:
            pass

 

        except:
            pass
        

    post_save.connect(create_profile_receiver, sender=settings.AUTH_USER_MODEL)
    post_save.connect(save_profile_receiver, sender=settings.AUTH_USER_MODEL)



class Profile(models.Model):
    user=models.OneToOneField(settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,null=True,blank=True)
    mobile=models.CharField(_("mobile"),null=True,blank=True, max_length=50)
    bio=models.CharField(_("bio"),null=True,blank=True, max_length=50)
    address=models.CharField(_("address"),null=True,blank=True, max_length=50)
    image_origin=models.ImageField(_("image"),null=True,blank=True, upload_to=IMAGE_FOLDER+"profile/", height_field=None, width_field=None, max_length=None)
    header_origin=models.ImageField(_("header_origin"),null=True,blank=True, upload_to=IMAGE_FOLDER+"profile/header/", height_field=None, width_field=None, max_length=None)
    enabled=models.BooleanField(_("enabled"),default=True)
    can_login=models.BooleanField(_("can login ?"),default=False)
    status=models.CharField(_("status"),choices=ProfileStatusEnum.choices,default=ProfileStatusEnum.AAA, max_length=50)
     
    def get_dashboard_url(self):
        return ''
        return reverse(APP_NAME+":dashboard",kwargs={'pk':self.pk})
    @property
    def first_name(self):
        return self.user.first_name
    @property
    def email(self):
        return self.user.email
    def full_tag(self,*args, **kwargs):
        return f"""
        <a href="{self.get_absolute_url()}" title="{self.name}">
               <img src="{self.image}" class="rounded-circle" width="48" alt="">
               {self.name}
        </a>

        """
    def media_tag(self):
        return f"""
            <div class="media">
                <img src="{self.image}" class="rounded-circle" width="48" alt="">

                <div class="media-body farsi text-right mr-2">

                    <div class="">
                        <a href="{self.get_absolute_url()}" title="{self.name}">
                            {self.name}
                        </a>

                    </div>
                    <div class="small text-secondary">{self.bio if self.bio is not None else ""}</div>
                </div>
            </div>
        """
    @property
    def image(self):
        if self.image_origin:
            return MEDIA_URL+str(self.image_origin)
        return STATIC_URL+APP_NAME+"/images/default-avatar.png"
    @property
    def header_image(self):
        if self.header_origin:
            return MEDIA_URL+str(self.header_origin)
        return STATIC_URL+"material-kit-pro/assets/img/city-profile.jpg"
    @property
    def last_name(self):
        return self.user.last_name
    @property
    def name(self):
        if self.user is not None:
            name=""
            if not (self.user.first_name is None or self.user.first_name==""):
                name=self.user.first_name+" "
                
            if not (self.user.last_name is None or self.user.last_name==""):
                name+=self.user.last_name+" "
            if not name=="":    
                return name
            else:
                return self.user.username
        
        else:
            return "profile "+str(self.pk)

    
    

    class Meta:
        verbose_name = _("Profile")
        verbose_name_plural = _("Profiles")

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse(APP_NAME+":profile", kwargs={"pk": self.pk})
    def get_reset_password_url(self):
        return ''
        return reverse(APP_NAME+":reset_password_view", kwargs={"profile_id": self.pk})

    def get_edit_url(self):
        return f"{ADMIN_URL}{APP_NAME}/profile/{self.pk}/change/"


