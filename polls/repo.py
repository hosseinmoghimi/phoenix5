from requests import request
from core.repo import ProfileRepo
from polls.apps import APP_NAME
from polls.models import Vote, Option, Poll

class PollRepo():  
    def __init__(self, *args, **kwargs):
        self.request = None
        self.user = None
        if 'request' in kwargs:
            self.request = kwargs['request']
            self.user = self.request.user
        if 'user' in kwargs:
            self.user = kwargs['user']
        
        self.objects=Poll.objects.all()
        self.profile=ProfileRepo(*args, **kwargs).me
       

    def poll(self, *args, **kwargs):
        pk=0
        if 'poll_id' in kwargs:
            pk= kwargs['poll_id']
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

    def add_poll(self,*args, **kwargs):
        if not self.user.has_perm(APP_NAME+".add_poll"):
            return None
        poll=Poll()
        if 'title' in kwargs:
            poll.title = kwargs['title']
        
        poll.creator=ProfileRepo(request=self.request).me
        poll.save()
        return poll


class OptionRepo():  
    def __init__(self, *args, **kwargs):
        self.request = None
        self.user = None
        if 'request' in kwargs:
            self.request = kwargs['request']
            self.user = self.request.user
        if 'user' in kwargs:
            self.user = kwargs['user']
        
        self.objects=Option.objects.all()
        self.profile=ProfileRepo(*args, **kwargs).me
       

    def option(self, *args, **kwargs):
        pk=0
        if 'option_id' in kwargs:
            pk= kwargs['option_id']
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

    def add_option(self,*args, **kwargs):
        poll=PollRepo(request=self.request).poll(poll_id=kwargs['poll_id'])
        if poll is None:
            return
        old_options=Option.objects.filter(title=kwargs['title']).filter(poll_id=poll.id)
        if len(old_options)>0:
            option=old_options.first()
            self.select_option(option_id=option.id)
            options=Option.objects.filter(poll_id=option.poll.id)
            return options
        if not self.user.has_perm(APP_NAME+".add_option"):
            return None
        option=Option()
        if 'title' in kwargs:
            option.title = kwargs['title']
        if 'poll_id' in kwargs:
            option.poll_id = kwargs['poll_id']
        
        option.creator=self.profile
        option.save()
        self.select_option(option_id=option.id)
        options=Option.objects.filter(poll_id=option.poll.id)
        return options


    def select_option(self,*args, **kwargs):
        if not self.user.has_perm(APP_NAME+".add_vote"):
            return None
        option=self.option(*args, **kwargs)
        if option is None:
            return

        Vote.objects.filter(profile_id=self.profile.pk).filter(option__poll_id=option.poll.id).delete()

        vote=Vote()
        vote.option=option
        vote.profile=self.profile
        vote.save()
        return vote

