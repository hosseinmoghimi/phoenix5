from .models import Blog,Feature,OurWork,Carousel
from authentication.repo import ProfileRepo

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
        if 'app_name' in kwargs:
            self.app_name = kwargs['app_name']
        return self.objects.filter(app_name=self.app_name)
    