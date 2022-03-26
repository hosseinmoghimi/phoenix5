from archive.models import Folder
from authentication.repo import ProfileRepo
from .apps import APP_NAME
    

class FolderRepo:
    def __init__(self, *args, **kwargs):
        self.request = None
        self.user = None
        if 'request' in kwargs:
            self.request = kwargs['request']
            self.user = self.request.user
        if 'user' in kwargs:
            self.user = kwargs['user']
        self.profile = ProfileRepo(user=self.user).me
        self.objects = Folder.objects.order_by('name')
        if self.user.has_perm(APP_NAME+".view_price"):
            self.objects = self.objects.all()
        elif self.profile is not None:
            self.objects = self.objects.filter(pk__gte=0)
        else:
            self.objects = self.objects.filter(pk=0)

    def create_folder(self,*args, **kwargs):
        if not self.user.has_perm(APP_NAME+".add_folder"):
            return
        print(kwargs)
        folder=Folder(*args, **kwargs)
        folder.save(*args, **kwargs)
        return folder
    def list(self, *args, **kwargs):
        objects = self.objects.all()
        if 'parent_id' in kwargs:
            objects = objects.filter(parent_id=kwargs['parent_id'])
        if 'for_home' in kwargs:
            objects = objects.filter(for_home=kwargs['for_home'])
        if 'search_for' in kwargs:
            objects = objects.filter(name__contains=kwargs['search_for'])
        return objects
    def get_root(self,*args, **kwargs):
        folder=Folder.objects.filter(pk=1).first()
        if folder is None:
            if not 'name' in kwargs:
                kwargs['name']="خانه"
            folder=Folder(*args, **kwargs)
            folder.save()
        return folder
    def folder(self,*args, **kwargs):
        if 'folder' in kwargs and kwargs['folder'] is not None:
            folder=kwargs['folder']
            return folder
        if 'name' in kwargs and kwargs['name'] is not None:
            return self.objects.filter(name= kwargs['name']).first()
        
        
        if 'pk' in kwargs and kwargs['pk'] is not None:
            pk=kwargs['pk']
        if 'id' in kwargs and kwargs['id'] is not None:
            pk=kwargs['id']
        if 'folder_id' in kwargs and kwargs['folder_id'] is not None:
            pk=kwargs['folder_id']
        
        if pk==1:
            folder=self.get_root(*args, **kwargs)
        else:
            folder=self.objects.filter(pk=pk).first()
        return folder 
   