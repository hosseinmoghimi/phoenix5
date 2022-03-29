from authentication.repo import ProfileRepo
from core.repo import PageRepo
from map.apps import APP_NAME
from map.models import Location, PageLocation

class LocationRepo():
    def __init__(self, *args, **kwargs):
        self.request = None
        self.user = None
        if 'request' in kwargs:
            self.request = kwargs['request']
            self.user = self.request.user
        if 'user' in kwargs:
            self.user = kwargs['user']
        self.profile=ProfileRepo(*args, **kwargs).me
        self.objects = Location.objects
    def list(self,*args, **kwargs):
        objects= self.objects
        if 'location_id' in kwargs:
            objects=objects.filter(location_id=kwargs['location_id'])
        if 'search_for' in kwargs:
            objects=objects.filter(title__contains=kwargs['search_for'])
        return objects.all()

    def location(self, *args, **kwargs):
        if 'location_id' in kwargs:
            return self.objects.filter(pk=kwargs['location_id']).first()
        if 'pk' in kwargs:
            return self.objects.filter(pk=kwargs['pk']).first()
        if 'id' in kwargs:
            return self.objects.filter(pk=kwargs['id']).first()
        if 'title' in kwargs:
            return self.objects.filter(pk=kwargs['title']).first()
            

    def add_location(self,*args, **kwargs):
        if not self.user.has_perm(APP_NAME+".add_location"):
            return None
        location1=""
        title=""
        if 'location' in kwargs:
            location1=kwargs['location']
        if 'title' in kwargs:
            title=kwargs['title']
        location=Location()
        location.title=title
        location.creator=self.profile
        location.location=location1
        location.latitude="gfgf"
        location.longitude="gfgf"
        location.save()
        if 'page_id' in kwargs and kwargs['page_id'] is not None and kwargs['page_id']>0:
            print(kwargs['page_id'])
            page_location=PageLocation()
            page_location.page_id=kwargs['page_id']
            page_location.location=location
            page_location.save()
        return location
    def search(self,search_for):
        objects = self.objects.filter(title__contains=search_for)
        return objects 

        
class PageLocationRepo():
    def __init__(self, *args, **kwargs):
        self.request = None
        self.user = None
        if 'request' in kwargs:
            self.request = kwargs['request']
            self.user = self.request.user
        if 'user' in kwargs:
            self.user = kwargs['user']
        self.profile=ProfileRepo(*args, **kwargs).me
        self.objects = PageLocation.objects
    def list(self,*args, **kwargs):
        objects= self.objects
        if 'page_id' in kwargs:
            objects=objects.filter(page_id=kwargs['page_id'])
        if 'location_id' in kwargs:
            objects=objects.filter(location_id=kwargs['location_id'])
        if 'search_for' in kwargs:
            objects=objects.filter(location__title__contains=kwargs['search_for'])
        return objects.all()
        

    def add_page_location(self,*args, **kwargs):
        if not self.user.has_perm(APP_NAME+".add_pagelocation"):
            return None
        location=LocationRepo(request=self.request).location(*args, **kwargs)
        page=PageRepo(request=self.request).page(*args, **kwargs)
        if page is None:
            return
        if location is None:
            return
        if location in page.location.all():
            return

        page_location=PageLocation()
        page_location.page=page
        page_location.location=location
        page_location.save()
        return page_location


    def page_location(self, *args, **kwargs):
        if 'page_location_id' in kwargs:
            return self.objects.filter(pk=kwargs['page_location_id']).first()
        if 'pagelocation_id' in kwargs:
            return self.objects.filter(pk=kwargs['pagelocation_id']).first()
        if 'pk' in kwargs:
            return self.objects.filter(pk=kwargs['pk']).first()
        if 'id' in kwargs:
            return self.objects.filter(pk=kwargs['id']).first()
        if 'title' in kwargs:
            return self.objects.filter(pk=kwargs['title']).first()
            

    def add_location(self,*args, **kwargs):
        if not self.user.has_perm(APP_NAME+".add_location"):
            return None
        location1=""
        title=""
        if 'location' in kwargs:
            location1=kwargs['location']
        if 'title' in kwargs:
            title=kwargs['title']
        location=Location()
        location.title=title
        location.creator=self.profile
        location.location=location1
        location.save()
        return location
    def search(self,search_for):
        objects = self.objects.filter(title__contains=search_for)
        return objects 

        