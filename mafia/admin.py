from django.contrib import admin

from mafia.models import GameScenario, Role,Game,Player,God,RolePlayer


admin.site.register(God)
admin.site.register(Role)
admin.site.register(RolePlayer)
admin.site.register(Game)
admin.site.register(Player)
admin.site.register(GameScenario)