from django.db import models
from core.models import  Page,_,reverse
from utility.utils import LinkHelper
from mafia.apps import APP_NAME

IMAGE_FOLDER="mafia/images/"


class Game(Page):
 
    class Meta:
        verbose_name = _("Role")
        verbose_name_plural = _("Roles")

    

    def save(self,*args, **kwargs):
        if self.app_name is None:
            self.app_name=APP_NAME
        if self.class_name is None:
            self.class_name='game'
        return super(Game,self).save()

  
 

class Role(Page):

    class Meta:
        verbose_name = _("Role")
        verbose_name_plural = _("Roles")


    def save(self,*args, **kwargs):
        if self.app_name is None:
            self.app_name=APP_NAME
        if self.class_name is None:
            self.class_name='role'
        return super(Role,self).save()

  
 

class Player(models.Model,LinkHelper):
    profile=models.ForeignKey("authentication.profile", verbose_name=_("profile"), on_delete=models.CASCADE)


    class Meta:
        verbose_name = _("Player")
        verbose_name_plural = _("Players")

    def __str__(self):
        return self.profile.name 


class God(models.Model,LinkHelper):
    profile=models.ForeignKey("authentication.profile", verbose_name=_("profile"), on_delete=models.CASCADE)

    

    class Meta:
        verbose_name = _("God")
        verbose_name_plural = _("Gods")

    def __str__(self):
        return self.profile.name
 

class RolePlayer(models.Model):
    role=models.ForeignKey("role", verbose_name=_("role"), on_delete=models.CASCADE)
    player=models.ForeignKey("player", verbose_name=_("player"), on_delete=models.CASCADE)
    game=models.ForeignKey("game", verbose_name=_("game"), on_delete=models.CASCADE)

    

    class Meta:
        verbose_name = _("RolePlayer")
        verbose_name_plural = _("RolePlayers")

    def __str__(self):
        return self.game.title

    def get_absolute_url(self):
        return reverse("RolePlayer_detail", kwargs={"pk": self.pk})
