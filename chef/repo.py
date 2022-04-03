from .models import Food
from django.db.models import Q
from authentication.repo import ProfileRepo
class FoodRepo():
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
        self.objects=Food.objects.all()
    def list(self,*args, **kwargs):
        objects=self.objects
        if 'search_for' in kwargs:
            return objects.filter(Q(title__contains=kwargs['search_for'])|Q(short_description__contains=kwargs['search_for']))
        return objects
    def food(self,*args, **kwargs):
        if 'food_id' in kwargs:
            return self.objects.filter(pk=kwargs['food_id']).first()
        if 'pk' in kwargs:
            return self.objects.filter(pk=kwargs['pk']).first()
        if 'id' in kwargs:
            return self.objects.filter(pk=kwargs['id']).first()
        if 'title' in kwargs:
            return self.objects.filter(pk=kwargs['title']).first()
