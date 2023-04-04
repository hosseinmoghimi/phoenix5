
from accounting.views import add_from_accounts_context
import json
from django.shortcuts import redirect, render,reverse
from django.views import View
from mafia.apps import APP_NAME
from core.views import CoreContext, MessageView,PageContext
from mafia.enums import RoleSideEnum
from mafia.forms import *
from mafia.repo import GameActRepo, GameRepo, GameScenarioRepo, GodRepo, PlayerRepo, RolePlayerRepo, RoleRepo
from mafia.serializers import GodSerializer,GameActSerializer, GameSerializer, PlayerSerializer, RolePlayerSerializer, RoleSerializer,GameScenarioSerializer

TEMPLATE_ROOT="mafia/"
LAYOUT_PARENT="phoenix/layout.html"
LAYOUT_WIDE_PARENT="phoenix/wide-layout.html"
def getContext(request,*args, **kwargs):
    context=CoreContext(request=request,app_name=APP_NAME)
    context['LAYOUT_PARENT']=LAYOUT_PARENT
    context['LAYOUT_WIDE_PARENT']=LAYOUT_WIDE_PARENT
    return context


class HomeView(View):
    def get(self,request,*args, **kwargs):
        context=getContext(request=request)
        return render(request,TEMPLATE_ROOT+"index.html",context)


class RolesView(View):
    def get(self,request,*args, **kwargs):
        context=getContext(request=request)
        roles=RoleRepo(request=request).list(*args, **kwargs)
        context['roles']=roles
        roles_s=json.dumps(RoleSerializer(roles,many=True).data)
        context['roles_s']=roles_s
        if request.user.has_perm(APP_NAME+".add_role"):
            context['sides']=(side[0] for side in RoleSideEnum.choices)
            context['add_role_form']=AddRoleForm()
        return render(request,TEMPLATE_ROOT+"roles.html",context)

class RoleView(View):
    def get(self,request,*args, **kwargs):
        context=getContext(request=request)
        role=RoleRepo(request=request).role(*args, **kwargs)
        context.update(PageContext(request=request,page=role))
        context['role']=role
        return render(request,TEMPLATE_ROOT+"role.html",context)


class GodsView(View):
    def get(self,request,*args, **kwargs):
        context=getContext(request=request)
        gods=GodRepo(request=request).list(*args, **kwargs)
        context['gods']=gods
        gods_s=json.dumps(GodSerializer(gods,many=True).data)
        context['gods_s']=gods_s
        if request.user.has_perm(APP_NAME+".add_god"):
            context['add_god_form']=AddGodForm()
            context.update(add_from_accounts_context(request=request))
        return render(request,TEMPLATE_ROOT+"gods.html",context)

class GodView(View):
    def get(self,request,*args, **kwargs):
        context=getContext(request=request)
        god=GodRepo(request=request).god(*args, **kwargs)
        context['god']=god
        return render(request,TEMPLATE_ROOT+"god.html",context)


class GameActView(View):
    def get(self,request,*args, **kwargs):
        context=getContext(request=request)
        game_acts=GameActRepo(request=request).list(*args, **kwargs)
        context['game_acts']=game_acts
        return render(request,TEMPLATE_ROOT+"game-acts.html",context)

class GameScenarioesView(View):
    def get(self,request,*args, **kwargs):
        context=getContext(request=request)
        game_scenarioes=GameScenarioRepo(request=request).list(*args, **kwargs)
        context['game_scenarioes']=game_scenarioes
        game_scenarioes_s=json.dumps(GameScenarioSerializer(game_scenarioes,many=True).data)
        context['game_scenarioes_s']=game_scenarioes_s
        if request.user.has_perm(APP_NAME+".add_god"):
            context['sides']=(side[0] for side in RoleSideEnum.choices)
            context['add_role_form']=AddRoleForm()
        return render(request,TEMPLATE_ROOT+"game-scenarioes.html",context)

class GameScenarioView(View):
    def get(self,request,*args, **kwargs):
        context=getContext(request=request)
        game_scenario=GameScenarioRepo(request=request).game_scenario(*args, **kwargs)
        context['game_scenario']=game_scenario

        roles=game_scenario.roles.all().order_by("side")
        context['roles']=roles
        roles_s=json.dumps(RoleSerializer(roles,many=True).data)
        context['roles_s']=roles_s

        return render(request,TEMPLATE_ROOT+"game-scenario.html",context)


class GamesView(View):
    def get(self,request,*args, **kwargs):
        context=getContext(request=request)
        games=GameRepo(request=request).list(*args, **kwargs)
        context['games']=games
        games_s=json.dumps(GameSerializer(games,many=True).data)
        context['games_s']=games_s
        if request.user.has_perm(APP_NAME+".add_game"):
            context['scenarioes']=GameScenarioRepo(request=request).list()
            context['gods']=GodRepo(request=request).list()
            context['add_game_form']=AddGameForm()
        return render(request,TEMPLATE_ROOT+"games.html",context)

class GameView(View):
    def get(self,request,*args, **kwargs):
        context=getContext(request=request)
        game=GameRepo(request=request).game(*args, **kwargs)
        # context.update(PageContext(request=request,page=game))
        context['game']=game

        if True:
            context['MAFIA']=RoleSideEnum.MAFIA
            context['CITIZEN']=RoleSideEnum.CITIZEN
            context['INDEPENDENT']=RoleSideEnum.INDEPENDENT
        # players
        if True:
            players=PlayerRepo(request=request).list()
            players_s=json.dumps(PlayerSerializer(players,many=True).data)
            context['players']=players
            context['players_s']=players_s

        # roles
        if True:
            roles=RoleRepo(request=request).list()
            roles_s=json.dumps(RoleSerializer(roles,many=True).data)
            context['roles']=roles
            context['roles_s']=roles_s
            selected_players=game.players.all()
            selected_players_s=json.dumps(PlayerSerializer(selected_players,many=True).data)
            context['selected_players_s']=selected_players_s
            selected_roles=[]
            for role_player in game.roleplayer_set.all():
                selected_roles.append(role_player.role)
            selected_roles_s=json.dumps(RoleSerializer(selected_roles,many=True).data)
            context['selected_roles_s']=selected_roles_s


        # role_players
        if True:
            role_players=RolePlayerRepo(request=request).list(game_id=game.id).order_by('role__side')
            role_players_s=json.dumps(RolePlayerSerializer(role_players,many=True).data)
            context['role_players_s']=role_players_s
            context['role_players']=role_players

        # game_acts
        if True:
            game_acts=GameActRepo(request=request).list(game_id=game.id).order_by('night')
            game_acts_s=json.dumps(GameActSerializer(game_acts,many=True).data)
            context['game_acts']=game_acts
            context['game_acts_s']=game_acts_s

        return render(request,TEMPLATE_ROOT+"game.html",context)


class AddGameView(View):
    def post(self,request,*args, **kwargs):
        if not request.user.has_perm(APP_NAME+".add_game"):
            return
        log=1
        fm=AddGameForm(request.POST)
        if fm.is_valid():
            log=2
            game=GameRepo(request=request).add_game(**fm.cleaned_data)
            if game is not None:
                log=3
                return redirect(game.get_absolute_url())
        mv=MessageView(request=request)
        mv.title="خطا در ایجاد بازی جدید "+str(log)
        return mv.response()





class InitializeView(View):
    def get(self,request,*args, **kwargs):
        if request.user.has_perm(APP_NAME+".add_game"):
            RoleRepo(request=request).initialize()
            GameScenarioRepo(request=request).initialize()
            return redirect(reverse(APP_NAME+":home"))
        mv=MessageView(request=request)
        mv.title="خطا در مقدار دهی اولیه"
        return mv.response()




class RolePlayersView(View):
    def get(self,request,*args, **kwargs):
        context=getContext(request=request)
        role_players=RolePlayerRepo(request=request).list(*args, **kwargs)
        context['role_players']=role_players
        role_players_s=json.dumps(RolePlayerSerializer(role_players,many=True).data)
        context['role_players_s']=role_players_s
        if request.user.has_perm(APP_NAME+".add_role"):
            context['sides']=(side[0] for side in RoleSideEnum.choices)
            context['add_role_form']=AddRoleForm()
        return render(request,TEMPLATE_ROOT+"role-players.html",context)

class RolePlayerView(View):
    def get(self,request,*args, **kwargs):
        context=getContext(request=request)
        role_player=RolePlayerRepo(request=request).role_player(*args, **kwargs)
        context['role_player']=role_player
        return render(request,TEMPLATE_ROOT+"role-player.html",context)


class PlayersView(View):
    def get(self,request,*args, **kwargs):
        context=getContext(request=request)
        players=PlayerRepo(request=request).list(*args, **kwargs)
        context['players']=players
        players_s=json.dumps(PlayerSerializer(players,many=True).data)
        context['players_s']=players_s
        # if request.user.has_perm(APP_NAME+".add_role"):
        #     context['sides']=(side[0] for side in RoleSideEnum.choices)
        #     context['add_role_form']=AddRoleForm()


        if request.user.has_perm(APP_NAME+".add_player"):
            context['add_player_form']=AddPlayerForm()
            context.update(add_from_accounts_context(request=request))

        return render(request,TEMPLATE_ROOT+"players.html",context)

class PlayerView(View):
    def get(self,request,*args, **kwargs):
        context=getContext(request=request)
        player=PlayerRepo(request=request).player(*args, **kwargs)
        context['player']=player

        
        role_players=RolePlayerRepo(request=request).list(*args, **kwargs).filter(player_id=player.id)
        context['role_players']=role_players
        role_players_s=json.dumps(RolePlayerSerializer(role_players,many=True).data)
        context['role_players_s']=role_players_s


        return render(request,TEMPLATE_ROOT+"player.html",context)


