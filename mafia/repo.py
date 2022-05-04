

from core.repo import ProfileRepo
from mafia.models import Role,Game,Player,RolePlayer,God
from mafia.apps import APP_NAME

class RoleRepo():  
    def __init__(self, *args, **kwargs):
        self.request = None
        self.user = None
        if 'request' in kwargs:
            self.request = kwargs['request']
            self.user = self.request.user
        if 'user' in kwargs:
            self.user = kwargs['user']
        
        self.objects=Role.objects.all()
        self.profile=ProfileRepo(*args, **kwargs).me
       

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
        if 'description' in kwargs:
            role.description = kwargs['description'] 
        role.save()
        return role


      