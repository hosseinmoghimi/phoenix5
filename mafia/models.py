from django.db import models
from core.models import  Page,_,reverse
from mafia.enums import GameStatusEnum, RoleSideEnum
from utility.utils import LinkHelper
from mafia.apps import APP_NAME

IMAGE_FOLDER="mafia/images/"

class Leage(models.Model,LinkHelper):
    title=models.CharField(_("title"), max_length=50)
    games=models.ManyToManyField("game", verbose_name=_("game"))
    class_name="leage"
    app_name=APP_NAME
    

    class Meta:
        verbose_name = _("Leage")
        verbose_name_plural = _("Leages")

    def __str__(self):
        return self.title
 

class Game(models.Model,LinkHelper):
    status=models.CharField(_("status"),choices=GameStatusEnum.choices,default=GameStatusEnum.INITIAL, max_length=50)
    date_added=models.DateTimeField(_("date_added"), auto_now=False, auto_now_add=True)
    god=models.ForeignKey("god", verbose_name=_("god"), on_delete=models.CASCADE)
    players=models.ManyToManyField("player",blank=True, verbose_name=_("players"))
    game_scenario=models.ForeignKey("gamescenario", verbose_name=_("scenario"), on_delete=models.CASCADE)
    class_name="game"
    app_name=APP_NAME

    def scenario(self):
        return self.game_scenario.title
    
    class Meta:
        verbose_name = _("Game")
        verbose_name_plural = _("Games")
    def __str__(self):
        return self.title

    @property
    def title(self):
        return "بازی شماره "+str(self.pk)

    def save(self,*args, **kwargs):        
        return super(Game,self).save()


class GameScenario(models.Model,LinkHelper):
    title=models.CharField(_("title"), max_length=50)
    description=models.CharField(_("description"),null=True,blank=True, max_length=5000)
    roles=models.ManyToManyField("role", verbose_name=_("roles"))
    class_name="gamescenario"
    app_name=APP_NAME
    class Meta:
        verbose_name = _("GameScenario")
        verbose_name_plural = _("GameScenarios")

    def __str__(self):
        return self.title


class Role(Page):
    side=models.CharField(_("side"),choices=RoleSideEnum.choices, max_length=50)
    wake_up_turn=models.IntegerField(_("نوبت بیدار شدن"),default=0)
    @property
    def color(self):
        if self.side==RoleSideEnum.CITIZEN:
            return 'success'
        if self.side==RoleSideEnum.MAFIA:
            return 'danger'
        if self.side==RoleSideEnum.INDEPENDENT:
            return 'primary'
    class Meta:
        verbose_name = _("Role")
        verbose_name_plural = _("Roles")


    def save(self,*args, **kwargs):
        if self.app_name is None:
            self.app_name=APP_NAME
        if self.class_name is None:
            self.class_name='role'
        return super(Role,self).save()

  
class GameAct(models.Model,LinkHelper):
    actor=models.ForeignKey("roleplayer",related_name="actor_acts", verbose_name=_("role_player"), on_delete=models.CASCADE)
    acted=models.ForeignKey("roleplayer", verbose_name=_("acted_acts"), on_delete=models.CASCADE)
    night=models.IntegerField(_("night?"))
    act=models.CharField(_("act"), max_length=50)
    score=models.IntegerField(_("score"),default=0)
    class_name="gameact"
    app_name=APP_NAME

    class Meta:
        verbose_name = _("GameAct")
        verbose_name_plural = _("GameActs")

    def __str__(self):
        return f"{self.act} : شب {self.night} : {self.actor.game.title}"
 

class Player(models.Model,LinkHelper):
    # profile=models.ForeignKey("authentication.profile", verbose_name=_("profile"), on_delete=models.CASCADE)
    account=models.ForeignKey("accounting.account", verbose_name=_("account"), on_delete=models.CASCADE)
    @property
    def score(self):
        return 4*23
    class_name="player"
    app_name=APP_NAME
    class Meta:
        verbose_name = _("Player")
        verbose_name_plural = _("Players")

    def __str__(self):
        return self.account.title 


class God(models.Model,LinkHelper):
    account=models.ForeignKey("accounting.account", verbose_name=_("account"), on_delete=models.CASCADE)

    class_name="god"
    app_name=APP_NAME

    class Meta:
        verbose_name = _("God")
        verbose_name_plural = _("Gods")

    def __str__(self):
        return self.account.title
 

class RolePlayer(models.Model,LinkHelper):
    role=models.ForeignKey("role", verbose_name=_("role"), on_delete=models.CASCADE)
    player=models.ForeignKey("player", verbose_name=_("player"), null=True,blank=True,on_delete=models.CASCADE)
    game=models.ForeignKey("game", verbose_name=_("game"), on_delete=models.CASCADE)
    class_name="roleplayer"
    app_name=APP_NAME
    

    class Meta:
        verbose_name = _("RolePlayer")
        verbose_name_plural = _("RolePlayers")

    def __str__(self):
        aa=str(self.player) if self.player is not None else ""
        return f"{aa} : {self.role.title} : {self.game.title}"
 