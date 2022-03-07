from .models import Category, Product
from django.db.models import Q
from authentication.repo import ProfileRepo
class ProductRepo():
    def __init__(self,*args, **kwargs):
        self.request=None
        self.user=None
        self.app_name=None
        if 'request' in kwargs:
            self.request=kwargs['request']
            self.user=self.request.user
        if 'user' in kwargs:
            self.user=kwargs['user']
        if 'app_name' in kwargs:
            self.app_name=kwargs['app_name']
        else:
            self.app_name=None
        self.profile=ProfileRepo(user=self.user).me
        self.objects=Product.objects.all()
    def list(self,*args, **kwargs):
        objects=self.objects
        if 'category_id' in kwargs:
            category=Category.objects.get(pk=kwargs['category_id'])
            if category is not None:
                return category.products.order_by('priority')
        if 'search_for' in kwargs:
            return objects.filter(Q(title__contains=kwargs['search_for'])|Q(short_description__contains=kwargs['search_for']))