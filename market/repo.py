from unicodedata import category
from accounting.repo import ProductRepo as ProductRepo_origin
from market.apps import APP_NAME
from market.models import Category, Supplier
from django.db.models import Q
from authentication.repo import ProfileRepo



class ProductRepo(ProductRepo_origin): 
    def list(self,*args, **kwargs):
        objects=self.objects
        if 'category_id' in kwargs:
            category=Category.objects.get(pk=kwargs['category_id'])
            if category is not None:
                return category.products.order_by('priority')

        if 'for_home' in kwargs:
            hps=objects=HomeProducts.objects.all()
            objects = objects.filter(Q(for_home=kwargs['for_home']))
        if 'search_for' in kwargs:
            return objects.filter(Q(title__contains=kwargs['search_for'])|Q(short_description__contains=kwargs['search_for']))
        return objects

class CategoryRepo():  
    def __init__(self, *args, **kwargs):
        self.request = None
        self.user = None
        if 'request' in kwargs:
            self.request = kwargs['request']
            self.user = self.request.user
        if 'user' in kwargs:
            self.user = kwargs['user']
        
        self.objects=Category.objects.all()
        self.profile=ProfileRepo(*args, **kwargs).me
       

    def category(self, *args, **kwargs):
        pk=0
        if 'category_id' in kwargs:
            pk= kwargs['category_id']
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

    def add_category(self,*args, **kwargs):
        if not self.user.has_perm(APP_NAME+".add_category"):
            return None
        parent_id=None
        category=Category()
        if 'title' in kwargs:
            category.title = kwargs['title']
            
        if 'parent_id' in kwargs:
            parent_id = kwargs['parent_id']
            if parent_id is not None and parent_id!=0:
                category.parent_id=parent_id

        category.save()
        return category


        
class SupplierRepo():  
    def __init__(self, *args, **kwargs):
        self.request = None
        self.user = None
        if 'request' in kwargs:
            self.request = kwargs['request']
            self.user = self.request.user
        if 'user' in kwargs:
            self.user = kwargs['user']
        
        self.objects=Supplier.objects.all()
        self.profile=ProfileRepo(*args, **kwargs).me
       

    def supplier(self, *args, **kwargs):
        pk=0
        if 'supplier_id' in kwargs:
            pk= kwargs['supplier_id']
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

    def add_supplier(self,*args, **kwargs):
        if not self.user.has_perm(APP_NAME+".add_supplier"):
            return None
        title=None
        if 'title' in kwargs:
            title = kwargs['title'] 

        supplier=Supplier()
        supplier.title=title
        supplier.save()
        return supplier


        