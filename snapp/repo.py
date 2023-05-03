from core.repo import Q,ProfileRepo,SUCCEED,FAILED
from accounting.repo import CategoryRepo,ProductRepo
from .models import Menu,APP_NAME



class MenuRepo():
    def __init__(self, *args, **kwargs):
        self.request = None
        self.user = None
        if 'request' in kwargs:
            self.request = kwargs['request']
            self.user = self.request.user
        if 'user' in kwargs:
            self.user = kwargs['user']
        
        self.objects=Menu.objects.all()
        self.profile=ProfileRepo(*args, **kwargs).me
       

    def menu(self, *args, **kwargs):
        pk=0
        if 'menu' in kwargs:
            return kwargs['menu']
        if 'menu_id' in kwargs:
            pk=kwargs['menu_id']
        elif 'pk' in kwargs:
            pk=kwargs['pk']
        elif 'id' in kwargs:
            pk=kwargs['id']
        return self.objects.filter(pk=pk).first()
     
    def list(self, *args, **kwargs):
        objects = self.objects
        if 'search_for' in kwargs:
            search_for=kwargs['search_for']
            objects = objects.filter(Q(title__contains=search_for))
        if 'for_home' in kwargs:
            objects = objects.filter(Q(for_home=kwargs['for_home']))
        if 'parent_id' in kwargs:
            objects=objects.filter(parent_id=kwargs['parent_id'])
        
        return objects.all()

    def add_menu(self,*args, **kwargs):
        if not self.user.has_perm(APP_NAME+".add_product"):
            return None
        menu=Menu()
  
        if 'title' in kwargs:
            menu.title = kwargs['title']
        if len(Menu.objects.filter(title=menu.title))>0:
            message="منوی وارد شده تکراری می باشد."
            return FAILED,None,message
        if menu.title is None or menu.title=="":
            message="عنوان منو نباید خالی باشد ."
            return FAILED,None,message

        menu.save() 
        message=menu.title +" با موفقیت افزوده شد."
        return SUCCEED,menu,message

 