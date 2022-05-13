import json
from django.shortcuts import render
from core.apps import APP_NAME
from core.repo import ParameterRepo
from polls.serializers import OptionSerializer, PollSerializer
from polls.repo import OptionRepo, PollRepo
from core.views import LAYOUT_PARENT, CoreContext,PageContext
from django.views import View
from .enums import POLLS_PARAMETER_NAMES
from polls.apps import APP_NAME
from .forms import AddOptionForm, AddPollForm
TEMPLATE_ROOT="polls/"
LAYOUT_PARENT="phoenix/layout.html"

def getContext(request,*args, **kwargs):
    context=CoreContext(request=request,app_name=APP_NAME,*args, **kwargs)
    context['LAYOUT_PARENT']=LAYOUT_PARENT
    return context

class HomeView(View):
    def get(self,request,*args, **kwargs):
        context=getContext(request=request,*args, **kwargs)
        param_repo=ParameterRepo(request=request,app_name=APP_NAME)
        context['POLLS_SYSTEM_TITLE']=param_repo.parameter(name=POLLS_PARAMETER_NAMES.POLLS_SYSTEM_TITLE)
        return render(request,TEMPLATE_ROOT+"index.html",context)
class PollsView(View):
    def get(self,request,*args, **kwargs):
        context=getContext(request=request,*args, **kwargs)
        polls=PollRepo(request=request).list(*args, **kwargs)
        context['polls']=polls
        polls_s=json.dumps(PollSerializer(polls,many=True).data)
        context['polls_s']=polls_s
        context['expand_polls']=True
        if request.user.has_perm(APP_NAME+".add_poll"):
            context['add_poll_form']=AddPollForm()
        return render(request,TEMPLATE_ROOT+"polls.html",context)


class PollView(View):
    def get(self,request,*args, **kwargs):
        context=getContext(request=request,*args, **kwargs)
        context['expand_options']=True
        param_repo=ParameterRepo(request=request,app_name=APP_NAME)
        context['POLLS_SYSTEM_TITLE']=param_repo.parameter(name=POLLS_PARAMETER_NAMES.POLLS_SYSTEM_TITLE)
        poll=PollRepo(request=request).poll(*args, **kwargs)
        context.update(PageContext(request=request,page=poll))
        context['toggle_page_like_form']=False
        context['dont_show_page_likes']=True
        poll_s=json.dumps(PollSerializer(poll).data)
        options=poll.option_set.all()
        options_s=json.dumps(OptionSerializer(options,many=True).data)
        context['poll']=poll
        context['poll_s']=poll_s
        context['options_s']=options_s
        if request.user.has_perm(APP_NAME+".add_option"):
            context['add_option_form']=AddOptionForm()
        return render(request,TEMPLATE_ROOT+"poll.html",context)

class OptionView(View):
    def get(self,request,*args, **kwargs):
        context=getContext(request=request,*args, **kwargs)
        option=OptionRepo(request=request).option(*args, **kwargs)
        option_s=json.dumps(OptionSerializer(option).data)
        if request.user.has_perm(APP_NAME+".add_option"):
            context['add_option_form']=AddOptionForm()
        return render(request,TEMPLATE_ROOT+"option.html",context)