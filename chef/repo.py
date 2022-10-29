from chef.apps import APP_NAME
from .models import Food, Host,Guest,Meal,ReservedMeal
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
    
    def add_food(self,*args, **kwargs):
        if not self.request.user.has_perm(APP_NAME+".add_food"):
            return
        food=Food(*args, **kwargs)
        food.save()
        return food



class GuestRepo():
    def __init__(self, *args, **kwargs):
        self.request = None
        self.user = None
        self.me = None
        self.objects = Guest.objects.filter(pk=0)
        if 'request' in kwargs:
            self.request = kwargs['request']
            self.user = self.request.user
        if 'user' in kwargs:
            self.user = kwargs['user']
        self.profile=ProfileRepo(request=self.request).me
        if self.profile is not None:
            self.me=Guest.objects.filter(account__profile_id=self.profile.id).first()
        if self.user.has_perm(APP_NAME+".view_guest"):
            self.objects=Guest.objects
    def guest(self, *args, **kwargs):
        
        if 'guest_id' in kwargs:
            pk=kwargs['guest_id']
        elif 'pk' in kwargs:
            pk=kwargs['pk']
        elif 'id' in kwargs:
            pk=kwargs['id']
        if pk==0:
            return self.me
        return self.objects.filter(pk=pk).first()
    
    def get(self, *args, **kwargs):
        return self.project(*args, **kwargs)

    def list(self, *args, **kwargs):
        objects = self.objects
        if 'search_for' in kwargs:
            objects = objects.filter(title__contains=kwargs['search_for'])
        if 'parent_id' in kwargs:
            objects=objects.filter(parent_id=kwargs['parent_id'])
        return objects.all()

  

class MealRepo():
    def __init__(self, *args, **kwargs):
        self.request = None
        self.user = None
        if 'request' in kwargs:
            self.request = kwargs['request']
            self.user = self.request.user
        if 'user' in kwargs:
            self.user = kwargs['user']
        
        self.objects=Meal.objects
    def meal(self, *args, **kwargs):
        
        if 'meal_id' in kwargs:
            pk=kwargs['meal_id']
        elif 'pk' in kwargs:
            pk=kwargs['pk']
        elif 'id' in kwargs:
            pk=kwargs['id']
        return self.objects.filter(pk=pk).first()
    
    def get(self, *args, **kwargs):
        return self.project(*args, **kwargs)

    def list(self, *args, **kwargs):
        objects = self.objects
        if 'search_for' in kwargs:
            objects = objects.filter(title__contains=kwargs['search_for'])
        if 'host_id' in kwargs:
            objects=objects.filter(host_id=kwargs['host_id'])
        # if 'is_reserved' in kwargs:
        #     guest=GuestRepo(request=self.request).me
        #     for meal in objects.all():
        #         meal.is_reserved(guest_id=guest.id)
        #         print(meal.reserved)
        # for meal in objects.all():
        #     print(meal.reserved)
        return objects.all()


    def add_meal(self,*args, **kwargs):
        meal=Meal()
        if 'title' in kwargs:
            meal.title=kwargs['title']
        if 'host_id' in kwargs:
            meal.host_id=kwargs['host_id']
        if 'date_served' in kwargs:
            meal.date_served=kwargs['date_served']
        food=FoodRepo(request=self.request).food(*args, **kwargs)
        host=HostRepo(request=self.request).host(*args, **kwargs)
        print(food)
        print(host)
        if 'meal_type' in kwargs:
            meal.meal_type=kwargs['meal_type']
        if 'max_reserve' in kwargs:
            meal.max_reserve=kwargs['max_reserve']
        meal.save()
        meal.foods.add(food)
        return meal

    

    

class ReservedMealRepo():
    def __init__(self, *args, **kwargs):
        self.request = None
        self.user = None
        if 'request' in kwargs:
            self.request = kwargs['request']
            self.user = self.request.user
        if 'user' in kwargs:
            self.user = kwargs['user']
        
        self.objects=ReservedMeal.objects


    def reserve_meal(self, *args, **kwargs):
        meal_id=kwargs['meal_id'] if 'meal_id' in kwargs else None
        guest_id=kwargs['guest_id'] if 'guest_id' in kwargs else None
        quantity=kwargs['quantity'] if 'quantity' in kwargs else 1
        me_guest=GuestRepo(request=self.request).me
        if guest_id is None:
            if me_guest is not None:
                guest_id=me_guest.id
        if guest_id is None or meal_id is None:
            return None
        reserved_meal=ReservedMeal.objects.filter(meal_id=meal_id).filter(guest_id=guest_id).first()
        if reserved_meal is not None:
            return
        # guest=GuestRepo(request=self.request).guest(*args, **kwargs)
        # if guest is None:
        #     return None
        if self.user.has_perm(APP_NAME+".add_reservedmeal") or (me_guest is not None and me_guest.id==guest_id):
            reserved_meal = ReservedMeal()
            reserved_meal.guest_id=guest_id
            reserved_meal.meal_id=meal_id
            reserved_meal.quantity=quantity
            reserved_meal.save()
            return reserved_meal
  

    def reserved_meal(self, *args, **kwargs):
        if 'meal_id' in kwargs and 'guest_id' in kwargs:
            meal_id=kwargs['meal_id']
            guest_id=kwargs['guest_id'] 
            if guest_id is None :
                guest=GuestRepo(request=self.request).me
                if guest is not None:
                    guest_id=guest.id
            return self.objects.filter(meal_id=meal_id).filter(guest_id= guest_id).first()
        pk=0
        if 'reserved_meal_id' in kwargs:
            pk=kwargs['reserved_meal_id']
        elif 'pk' in kwargs:
            pk=kwargs['pk']
        elif 'id' in kwargs:
            pk=kwargs['id']
        return self.objects.filter(pk=pk).first()
    
    def get(self, *args, **kwargs):
        return self.project(*args, **kwargs)

    def list(self, *args, **kwargs):
        objects = self.objects
        if 'meal_id' in kwargs:
            objects = objects.filter(meal_id=kwargs['meal_id'])
        if 'guest_id' in kwargs:
            objects = objects.filter(guest_id=kwargs['guest_id'])
        if 'parent_id' in kwargs:
            objects=objects.filter(parent_id=kwargs['parent_id'])
        return objects.all()
    def serve_meal(self, *args, **kwargs):
        me_host=HostRepo(request=self.request).me
        reserved_meal=self.reserved_meal(*args, **kwargs)
        if self.user.has_perm(APP_NAME+".change_reservedmeal"):
            pass
        elif me_host is not None and me_host.id==reserved_meal.host.id:
            pass
        else:
            return
        if reserved_meal is None or reserved_meal.date_served is not None:
            return
        reserved_meal.date_served=timezone.now()
        reserved_meal.save() 
        return reserved_meal
            
    def unserve_meal(self, *args, **kwargs):
        reserved_meal=self.reserved_meal(*args, **kwargs)
        if reserved_meal is None or reserved_meal.date_served is None:
            return
        reserved_meal.date_served=None
        reserved_meal.save() 
        return reserved_meal
            
  
    def unreserve_meal(self, *args, **kwargs):
        reserved_meal=self.reserved_meal(*args, **kwargs)
        if reserved_meal is None:
            return
        meal=reserved_meal.meal
        reserved_meal.delete()
        return meal
 

  
class HostRepo():
    def __init__(self, *args, **kwargs):
        self.request = None
        self.user = None
        self.me=None
        self.profile=None
        if 'request' in kwargs:
            self.request = kwargs['request']
            self.user = self.request.user
        if 'user' in kwargs:
            self.user = kwargs['user']  
        self.me=ProfileRepo(request=self.request).me
        self.me=Host.objects.filter(account__profile=self.profile).first()
        self.objects=Host.objects
    def host(self, *args, **kwargs):
        pk=0
        if 'host_id' in kwargs:
            pk=kwargs['host_id']
        elif 'pk' in kwargs:
            pk=kwargs['pk']
        elif 'id' in kwargs:
            pk=kwargs['id']
        return self.objects.filter(pk=pk).first()
    
    def get(self, *args, **kwargs):
        return self.project(*args, **kwargs)

    def list(self, *args, **kwargs):
        objects = self.objects
        if 'search_for' in kwargs:
            objects = objects.filter(title__contains=kwargs['search_for'])
        if 'parent_id' in kwargs:
            objects=objects.filter(parent_id=kwargs['parent_id'])
        return objects.all()


    def add_host(self, *args, **kwargs):
        if not self.request.user.has_perm(APP_NAME+".add_host"):
            return
        host=Host()
        if 'profile_id' in kwargs:
            host.profile_id = kwargs['profile_id']
        host.save()
        return host
  
