from web.apps import APP_NAME
from .models import Blog,Feature, OurTeam,OurWork,Carousel, PricingItem, PricingPage, Testimonial
from django.db.models import Q
from authentication.repo import ProfileRepo

class CarouselRepo:
    def __init__(self,*args, **kwargs):
        self.request = None
        self.app_name=""
        self.user = None
        if 'request' in kwargs:
            self.request = kwargs['request']
            self.user = self.request.user
        if 'user' in kwargs:
            self.user = kwargs['user']
        if 'app_name' in kwargs:
            self.app_name = kwargs['app_name']
        self.objects = Carousel.objects.order_by('priority')
        self.me=ProfileRepo(user=self.user).me
    def list(self,*args, **kwargs):
        objects=self.objects
        if 'app_name' in kwargs:
            self.app_name = kwargs['app_name']
        return objects
    
class FeatureRepo:
    def __init__(self,*args, **kwargs):
        self.request = None
        self.user = None
        if 'request' in kwargs:
            self.request = kwargs['request']
            self.user = self.request.user
        if 'user' in kwargs:
            self.user = kwargs['user']
        self.objects = Feature.objects
        self.me=ProfileRepo(user=self.user).me
    def list(self,*args, **kwargs):
        objects= self.objects.all()
        if 'search_for' in kwargs:
            search_for=kwargs['search_for']
            objects=objects.filter(Q(title__contains=search_for) | Q(meta_data__contains=search_for)|Q(description__contains=search_for))
        if 'for_home' in kwargs:
            objects=objects.filter(for_home=kwargs['for_home'])
        return objects
    def feature(self,*args, **kwargs):
        pk=0
        if 'feature_id' in kwargs:
            pk=kwargs['feature_id']
        elif 'pk' in kwargs:
            pk=kwargs['pk']
        elif 'id' in kwargs:
            pk=kwargs['id']
        return self.objects.filter(pk=pk).first()
   
   
class BlogRepo:
    def __init__(self,*args, **kwargs):
        self.request = None
        self.user = None
        if 'request' in kwargs:
            self.request = kwargs['request']
            self.user = self.request.user
        if 'user' in kwargs:
            self.user = kwargs['user']
        self.objects = Blog.objects.order_by('priority')
        self.me=ProfileRepo(user=self.user).me

    def list(self,*args, **kwargs):
        objects= self.objects.all()
        if 'for_home' in kwargs:
            objects=objects.filter(for_home=kwargs['for_home'])
        if 'author_id' in kwargs:
            objects=objects.filter(author_id=kwargs['author_id'])
        if 'our_team_id' in kwargs:
            objects=objects.filter(author_id=kwargs['our_team_id'])
        if 'search_for' in kwargs:
            search_for=kwargs['search_for']
            objects=objects.filter(Q(title__contains=search_for) | Q(meta_data__contains=search_for)|Q(description__contains=search_for))
        return objects

    def blog(self,*args, **kwargs):
        pk=0
        if 'blog_id' in kwargs:
            pk=kwargs['blog_id']
        elif 'pk' in kwargs:
            pk=kwargs['pk']
        elif 'id' in kwargs:
            pk=kwargs['id']
        return self.objects.filter(pk=pk).first()
    def add_blog(self,*args, **kwargs):
        if not self.user.has_perm(APP_NAME+".add_blog"):
            return
        
        blog=Blog()
        if 'title' in kwargs:
            blog.title=kwargs['title']
        if 'for_home' in kwargs:
            blog.for_home=kwargs['for_home']
        
        blog.save()
        return blog



   
class PricingPageRepo:
    def __init__(self,*args, **kwargs):
        self.request = None
        self.user = None
        if 'request' in kwargs:
            self.request = kwargs['request']
            self.user = self.request.user
        if 'user' in kwargs:
            self.user = kwargs['user']
        self.objects = PricingPage.objects.order_by('priority')
        self.me=ProfileRepo(user=self.user).me

    def list(self,*args, **kwargs):
        objects= self.objects.all()
        if 'for_home' in kwargs:
            objects=objects.filter(for_home=kwargs['for_home'])
        if 'author_id' in kwargs:
            objects=objects.filter(author_id=kwargs['author_id'])
        if 'our_team_id' in kwargs:
            objects=objects.filter(author_id=kwargs['our_team_id'])
        if 'search_for' in kwargs:
            search_for=kwargs['search_for']
            objects=objects.filter(Q(title__contains=search_for) | Q(meta_data__contains=search_for)|Q(description__contains=search_for))
        return objects

    def pricing_page(self,*args, **kwargs):
        pk=0
        if 'pricing_page_id' in kwargs:
            pk=kwargs['pricing_page_id']
        elif 'pk' in kwargs:
            pk=kwargs['pk']
        elif 'id' in kwargs:
            pk=kwargs['id']
        return self.objects.filter(pk=pk).first()
    def add_pricing_page(self,*args, **kwargs):
        if not self.user.has_perm(APP_NAME+".add_pricingpage"):
            return
        
        pricing_page=PricingPage()
        if 'title' in kwargs:
            pricing_page.title=kwargs['title']
        if 'for_home' in kwargs:
            pricing_page.for_home=kwargs['for_home']
        
        pricing_page.save()
        return pricing_page


   
class PricingItemRepo:
    def __init__(self,*args, **kwargs):
        self.request = None
        self.user = None
        if 'request' in kwargs:
            self.request = kwargs['request']
            self.user = self.request.user
        if 'user' in kwargs:
            self.user = kwargs['user']
        self.objects = PricingItem.objects.order_by('priority')
        self.me=ProfileRepo(user=self.user).me

    def list(self,*args, **kwargs):
        objects= self.objects.all()
        if 'for_home' in kwargs:
            objects=objects.filter(for_home=kwargs['for_home'])
        if 'author_id' in kwargs:
            objects=objects.filter(author_id=kwargs['author_id'])
        if 'our_team_id' in kwargs:
            objects=objects.filter(author_id=kwargs['our_team_id'])
        if 'search_for' in kwargs:
            search_for=kwargs['search_for']
            objects=objects.filter(Q(title__contains=search_for) | Q(meta_data__contains=search_for)|Q(description__contains=search_for))
        return objects

    def pricing_item(self,*args, **kwargs):
        pk=0
        if 'pricing_item_id' in kwargs:
            pk=kwargs['pricing_item_id']
        elif 'pk' in kwargs:
            pk=kwargs['pk']
        elif 'id' in kwargs:
            pk=kwargs['id']
        return self.objects.filter(pk=pk).first()
    def add_pricing_item(self,*args, **kwargs):
        if not self.user.has_perm(APP_NAME+".add_pricingitem"):
            return
        
        pricing_item=PricingItem()
        if 'title' in kwargs:
            pricing_item.title=kwargs['title']
        if 'for_home' in kwargs:
            pricing_item.for_home=kwargs['for_home']
        
        pricing_item.save()
        return pricing_item



class OurWorkRepo:
    def __init__(self,*args, **kwargs):
        self.request = None
        self.user = None
        if 'request' in kwargs:
            self.request = kwargs['request']
            self.user = self.request.user
        if 'user' in kwargs:
            self.user = kwargs['user']
        self.objects = OurWork.objects
        self.me=ProfileRepo(user=self.user).me
    def list(self,*args, **kwargs):
        objects= self.objects.all()
        if 'for_home' in kwargs:
            objects=objects.filter(for_home=kwargs['for_home'])
        if 'author_id' in kwargs:
            objects=objects.filter(author_id=kwargs['author_id'])
        if 'our_team_id' in kwargs:
            objects=objects.filter(author_id=kwargs['our_team_id'])
        if 'search_for' in kwargs:
            search_for=kwargs['search_for']
            objects=objects.filter(Q(title__contains=search_for) | Q(meta_data__contains=search_for)|Q(description__contains=search_for))
        return objects
    def our_work(self,*args, **kwargs):
        pk=0
        if 'our_work_id' in kwargs:
            pk=kwargs['our_work_id']
        elif 'pk' in kwargs:
            pk=kwargs['pk']
        elif 'id' in kwargs:
            pk=kwargs['id']
        return self.objects.filter(pk=pk).first()
    def add_our_work(self,*args, **kwargs):
        if not self.user.has_perm(APP_NAME+".add_ourwork"):
            return
        
        our_work=OurWork()
        if 'title' in kwargs:
            our_work.title=kwargs['title']
        if 'for_home' in kwargs:
            our_work.for_home=kwargs['for_home']
        
        our_work.save()
        return our_work


class OurTeamRepo:
    def __init__(self,*args, **kwargs):
        self.request = None
        self.user = None
        if 'request' in kwargs:
            self.request = kwargs['request']
            self.user = self.request.user
        if 'user' in kwargs:
            self.user = kwargs['user']
        self.objects = OurTeam.objects.order_by('priority')
        self.me=ProfileRepo(user=self.user).me
    def list(self,*args, **kwargs):
        objects= self.objects.all()
        if 'for_home' in kwargs:
            objects=objects.filter(for_home=kwargs['for_home'])
        return objects
    def our_team(self,*args, **kwargs):
        pk=0
        if 'our_team_id' in kwargs:
            pk=kwargs['our_team_id']
        elif 'pk' in kwargs:
            pk=kwargs['pk']
        elif 'id' in kwargs:
            pk=kwargs['id']
        return self.objects.filter(pk=pk).first()
   
   


class TestimonialRepo:
    def __init__(self,*args, **kwargs):
        self.request = None
        self.user = None
        if 'request' in kwargs:
            self.request = kwargs['request']
            self.user = self.request.user
        if 'user' in kwargs:
            self.user = kwargs['user']
        self.objects = Testimonial.objects.order_by('priority')
        self.me=ProfileRepo(user=self.user).me
    def list(self,*args, **kwargs):
        objects= self.objects.all()
        if 'for_home' in kwargs:
            objects=objects.filter(for_home=kwargs['for_home'])
        return objects
    def testimonial(self,*args, **kwargs):
        pk=0
        if 'testimonial_id' in kwargs:
            pk=kwargs['testimonial_id']
        elif 'pk' in kwargs:
            pk=kwargs['pk']
        elif 'id' in kwargs:
            pk=kwargs['id']
        return self.objects.filter(pk=pk).first()
   
  