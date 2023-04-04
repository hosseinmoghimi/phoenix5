

from core.repo import ProfileRepo,FAILED,SUCCEED
from mafia.enums import RoleSideEnum
from mafia.models import GameAct, Role,Game,Player,RolePlayer,God,GameScenario
from mafia.apps import APP_NAME
from mafia.default import init_roles,init_scenarioes

class RoleRepo():
    def __init__(self, *args, **kwargs):
        self.request = None
        self.user = None
        if 'request' in kwargs:
            self.request = kwargs['request']
            self.user = self.request.user
        if 'user' in kwargs:
            self.user = kwargs['user']
        
        self.objects=Role.objects.all().order_by('side')
        self.profile=ProfileRepo(*args, **kwargs).me
       
    def initialize(self,*args, **kwargs):
        init_roles()
        


    def role(self, *args, **kwargs):
        pk=0
        if 'role_id' in kwargs:
            pk= kwargs['role_id']
            return self.objects.filter(pk=pk).first()
       
        elif 'pk' in kwargs:
            pk=kwargs['pk']
            return self.objects.filter(pk=pk).first()
        elif 'id' in kwargs:
            pk=kwargs['id']
            return self.objects.filter(pk=pk).first()
        elif 'title' in kwargs:
            title=kwargs['title']
            return self.objects.filter(title=title).first()
     
    def list(self, *args, **kwargs):
        objects = self.objects
        if 'search_for' in kwargs:
            search_for=kwargs['search_for']
            objects = objects.filter(Q(title__contains=search_for)|Q(short_description__contains=search_for)|Q(description__contains=search_for))
        if 'for_home' in kwargs:
            objects = objects.filter(Q(for_home=kwargs['for_home']))
        if 'parent_id' in kwargs:
            objects=objects.filter(parent_id=kwargs['parent_id'])
        return objects.all()

    def add_role(self,*args, **kwargs):
        if not self.user.has_perm(APP_NAME+".add_role"):
            return None
        role=Role()
        if 'title' in kwargs:
            role.title = kwargs['title']
        if 'side' in kwargs:
            role.side = kwargs['side'] 
        if 'description' in kwargs:
            role.description = kwargs['description'] 
        role.save()
        return role


class GameScenarioRepo():  
    def __init__(self, *args, **kwargs):
        self.request = None
        self.user = None
        if 'request' in kwargs:
            self.request = kwargs['request']
            self.user = self.request.user
        if 'user' in kwargs:
            self.user = kwargs['user']
        
        self.objects=GameScenario.objects.all()
        self.profile=ProfileRepo(*args, **kwargs).me
    
    
    def initialize(self,*args, **kwargs):
        init_scenarioes()


    def game_scenario(self, *args, **kwargs):
        pk=0
        if 'game_scenario_id' in kwargs:
            pk= kwargs['game_scenario_id']
            return self.objects.filter(pk=pk).first()
       
        elif 'pk' in kwargs:
            pk=kwargs['pk']
            return self.objects.filter(pk=pk).first()
        elif 'id' in kwargs:
            pk=kwargs['id']
            return self.objects.filter(pk=pk).first()
     
    def list(self, *args, **kwargs):
        objects = self.objects
        if 'search_for' in kwargs:
            search_for=kwargs['search_for']
            objects = objects.filter(Q(title__contains=search_for)|Q(short_description__contains=search_for)|Q(description__contains=search_for))
        if 'for_home' in kwargs:
            objects = objects.filter(Q(for_home=kwargs['for_home']))
        if 'parent_id' in kwargs:
            objects=objects.filter(parent_id=kwargs['parent_id'])
        return objects.all()

    def add_game_scenario(self,*args, **kwargs):
        if not self.user.has_perm(APP_NAME+".add_gamescenario"):
            return None
        game_scenario=GameScenario()
        if 'title' in kwargs:
            game_scenario.title = kwargs['title'] 
        if 'description' in kwargs:
            game_scenario.description = kwargs['description'] 
        game_scenario.save()
        return game_scenario


class GameRepo():
    def __init__(self, *args, **kwargs):
        self.request = None
        self.user = None
        if 'request' in kwargs:
            self.request = kwargs['request']
            self.user = self.request.user
        if 'user' in kwargs:
            self.user = kwargs['user']
        
        self.objects=Game.objects.all()
        self.profile=ProfileRepo(*args, **kwargs).me

    def game(self, *args, **kwargs):
        pk=0
        if 'game_id' in kwargs:
            pk= kwargs['game_id']
            return self.objects.filter(pk=pk).first()
       
        elif 'pk' in kwargs:
            pk=kwargs['pk']
            return self.objects.filter(pk=pk).first()
        elif 'id' in kwargs:
            pk=kwargs['id']
            return self.objects.filter(pk=pk).first()
     
    def list(self, *args, **kwargs):
        objects = self.objects
        if 'search_for' in kwargs:
            search_for=kwargs['search_for']
            objects = objects.filter(Q(title__contains=search_for)|Q(short_description__contains=search_for)|Q(description__contains=search_for))
        if 'for_home' in kwargs:
            objects = objects.filter(Q(for_home=kwargs['for_home']))
        if 'parent_id' in kwargs:
            objects=objects.filter(parent_id=kwargs['parent_id'])
        return objects.all()

    def add_game(self,*args, **kwargs):
        if not self.user.has_perm(APP_NAME+".add_game"):
            return None
        game=Game()
        if 'title' in kwargs and kwargs['title'] is not None and not kwargs['title']=="":
            game.title = kwargs['title'] 
        
        if 'game_scenario_id' in kwargs:
            game.game_scenario_id = kwargs['game_scenario_id']
                
        if 'god_id' in kwargs:
            game.god_id = kwargs['god_id']
        if 'description' in kwargs:
            game.description = kwargs['description'] 
        if 'status' in kwargs:
            game.status = kwargs['status']

        
            
        game.save()
        if 'game_scenario_id' in kwargs:
            game_scenario=GameScenario.objects.filter(pk=kwargs['game_scenario_id']).first()
            if game_scenario is not None:
                roles=game_scenario.roles.all()
                for role in roles:
                    role_player=RolePlayer()
                    role_player.role_id=role.id
                    role_player.game_id=game.id
                    role_player.player=None
                    role_player.save()
        return game



    def add_role_to_game(self,*args, **kwargs):
        if not self.user.has_perm(APP_NAME+".add_roleplayer"):
            return None
        role_player=RolePlayer(*args, **kwargs)
        role_player.save()
        return role_player


class PlayerRepo():  
    def __init__(self, *args, **kwargs):
        self.request = None
        self.user = None
        if 'request' in kwargs:
            self.request = kwargs['request']
            self.user = self.request.user
        if 'user' in kwargs:
            self.user = kwargs['user']
        
        self.objects=Player.objects.all()
        self.profile=ProfileRepo(*args, **kwargs).me
       

    def player(self, *args, **kwargs):
        pk=0
        if 'player_id' in kwargs:
            pk= kwargs['player_id']
            return self.objects.filter(pk=pk).first()
       
        elif 'pk' in kwargs:
            pk=kwargs['pk']
            return self.objects.filter(pk=pk).first()
        elif 'id' in kwargs:
            pk=kwargs['id']
            return self.objects.filter(pk=pk).first()
     
    def list(self, *args, **kwargs):
        objects = self.objects
        if 'search_for' in kwargs:
            search_for=kwargs['search_for']
            objects = objects.filter(Q(title__contains=search_for)|Q(short_description__contains=search_for)|Q(description__contains=search_for))
        if 'for_home' in kwargs:
            objects = objects.filter(Q(for_home=kwargs['for_home']))
        if 'parent_id' in kwargs:
            objects=objects.filter(parent_id=kwargs['parent_id'])
        return objects.all()

    def add_player(self,*args, **kwargs):
        player,message,result=None,"",FAILED
        if not self.user.has_perm(APP_NAME+".add_player"):
            message="شما مجوز لازم برای ایجاد بازیکن جدید ندارید ."
            return player,message,result
        olds=Player.objects.filter(account_id=kwargs['account_id'])
        if len(olds)>0:
            message="این حساب قبلا در لیست بازیکنان ایجاد شده است ."
            return player,message,result
        player=Player()
        if 'account_id' in kwargs:
            player.account_id = kwargs['account_id'] 
         
        player.save()
        result=SUCCEED
        message=f"""بازیکن جدید "{player.account.title}" با موفقیت افزوده شد ."""
        return player,message,result


class GodRepo():  
    def __init__(self, *args, **kwargs):
        self.request = None
        self.user = None
        if 'request' in kwargs:
            self.request = kwargs['request']
            self.user = self.request.user
        if 'user' in kwargs:
            self.user = kwargs['user']
        
        self.objects=God.objects.all()
        self.profile=ProfileRepo(*args, **kwargs).me
       

    def god(self, *args, **kwargs):
        pk=0
        if 'god' in kwargs:
            pk= kwargs['god']
            return self.objects.filter(pk=pk).first()
       
        elif 'pk' in kwargs:
            pk=kwargs['pk']
            return self.objects.filter(pk=pk).first()
        elif 'id' in kwargs:
            pk=kwargs['id']
            return self.objects.filter(pk=pk).first()
     
    def list(self, *args, **kwargs):
        objects = self.objects
        if 'search_for' in kwargs:
            search_for=kwargs['search_for']
            objects = objects.filter(Q(title__contains=search_for)|Q(short_description__contains=search_for)|Q(description__contains=search_for))
        if 'for_home' in kwargs:
            objects = objects.filter(Q(for_home=kwargs['for_home']))
        if 'parent_id' in kwargs:
            objects=objects.filter(parent_id=kwargs['parent_id'])
        return objects.all()

    def add_god(self,*args, **kwargs):
        god,message,result=None,"",FAILED

        
        if not self.user.has_perm(APP_NAME+".add_god"):
            message="شما مجوز لازم برای ایجاد گاد جدید ندارید ."
            return god,message,result
        olds=God.objects.filter(account_id=kwargs['account_id'])
        if len(olds)>0:
            message="این حساب قبلا در لیست گادها ایجاد شده است ."
            return god,message,result
        
        
        god=God()
        if 'account_id' in kwargs:
            god.account_id = kwargs['account_id'] 
         
        god.save()
        result=SUCCEED
        message="با موفقیت افزوده شد."
        return god,message,result


class GameActRepo():  
    def __init__(self, *args, **kwargs):
        self.request = None
        self.user = None
        if 'request' in kwargs:
            self.request = kwargs['request']
            self.user = self.request.user
        if 'user' in kwargs:
            self.user = kwargs['user']
        
        self.objects=GameAct.objects.all()
        self.profile=ProfileRepo(*args, **kwargs).me
       

    def game_act(self, *args, **kwargs):
        pk=0
        if 'game_act' in kwargs:
            pk= kwargs['game_act']
            return self.objects.filter(pk=pk).first()
        elif 'game_act_id' in kwargs:
            pk=kwargs['game_act_id']
            return self.objects.filter(pk=pk).first()
       
        elif 'pk' in kwargs:
            pk=kwargs['pk']
            return self.objects.filter(pk=pk).first()
        elif 'id' in kwargs:
            pk=kwargs['id']
            return self.objects.filter(pk=pk).first()
     
    def list(self, *args, **kwargs):
        objects = self.objects
        if 'search_for' in kwargs:
            search_for=kwargs['search_for']
            objects = objects.filter(Q(title__contains=search_for)|Q(short_description__contains=search_for)|Q(description__contains=search_for))
        if 'for_home' in kwargs:
            objects = objects.filter(Q(for_home=kwargs['for_home']))
        if 'parent_id' in kwargs:
            objects=objects.filter(parent_id=kwargs['parent_id'])
        if 'game_id' in kwargs:
            objects=objects.filter(actor__game_id=kwargs['game_id'])
        return objects.all()

    def add_game_act(self,*args, **kwargs):
        if not self.user.has_perm(APP_NAME+".add_god"):
            return None
        game_act=GameAct()
        if 'role_player_id' in kwargs:
            game_act.role_player_id = kwargs['role_player_id'] 
         
        game_act.save()
        return game_act


class RolePlayerRepo():
    def __init__(self, *args, **kwargs):
        self.request = None
        self.user = None
        if 'request' in kwargs:
            self.request = kwargs['request']
            self.user = self.request.user
        if 'user' in kwargs:
            self.user = kwargs['user']
        
        self.objects=RolePlayer.objects
        self.profile=ProfileRepo(*args, **kwargs).me
       

    def role_player(self, *args, **kwargs):
        pk=0
        if 'role_player_id' in kwargs:
            pk= kwargs['role_player_id']
            return self.objects.filter(pk=pk).first()
       
        elif 'pk' in kwargs:
            pk=kwargs['pk']
            return self.objects.filter(pk=pk).first()
        elif 'id' in kwargs:
            pk=kwargs['id']
            return self.objects.filter(pk=pk).first()
     
    def list(self, *args, **kwargs):
        objects = self.objects
        if 'search_for' in kwargs:
            search_for=kwargs['search_for']
            objects = objects.filter(Q(title__contains=search_for)|Q(short_description__contains=search_for)|Q(description__contains=search_for))
        if 'for_home' in kwargs:
            objects = objects.filter(Q(for_home=kwargs['for_home']))
        if 'game_id' in kwargs:
            objects=objects.filter(game_id=kwargs['game_id'])
        return objects.all()

    def add_role_player(self,*args, **kwargs):
        if not self.user.has_perm(APP_NAME+".add_roleplayer"):
            return None
        role_player=RolePlayer()

        if 'player_id' in kwargs and kwargs['player_id'] is not None and not kwargs['player_id']=="":
            role_player.player_id = kwargs['player_id']

        if 'role_id' in kwargs and kwargs['role_id'] is not None and not kwargs['role_id']=="":
            role_player.role_id = kwargs['role_id']
            
        if 'game_id' in kwargs and kwargs['game_id'] is not None and not kwargs['game_id']=="":
            role_player.game_id = kwargs['game_id']
            
        role_player.save()
        return role_player



      