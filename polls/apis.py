from core.apis import APIView,SUCCEED,FAILED,JsonResponse
from polls.forms import *
from polls.repo import OptionRepo, PollRepo
from polls.serializers import PollSerializer,OptionSerializer,VoteSerializer

class AddPollApi(APIView):
    def post(self,request,*args, **kwargs):
        context={}
        context['result']=FAILED
        log=2
        fm=AddPollForm(request.POST)
        if fm.is_valid():
            log=3
            cd=fm.cleaned_data
            poll=PollRepo(request=request).add_poll(**cd)
            if poll is not None:
                log=4
                context['result']=SUCCEED
                context['poll']=PollSerializer(poll).data
        context['log']=log
        return JsonResponse(context)

class AddOptionApi(APIView):
    def post(self,request,*args, **kwargs):
        context={}
        context['result']=FAILED
        log=2
        fm=AddOptionForm(request.POST)
        if fm.is_valid():
            log=3
            cd=fm.cleaned_data
            option=OptionRepo(request=request).add_option(**cd)
            if option is not None:
                log=4
                context['result']=SUCCEED
                context['option']=OptionSerializer(option).data
        context['log']=log
        return JsonResponse(context)



class SelectOptionApi(APIView):
    def post(self,request,*args, **kwargs):
        context={}
        context['result']=FAILED
        log=2
        fm=SelectOptionForm(request.POST)
        if fm.is_valid():
            log=3
            cd=fm.cleaned_data
            vote=OptionRepo(request=request).select_option(**cd)
            if vote is not None:
                log=4
                context['result']=SUCCEED
                context['vote']=VoteSerializer(vote).data
                context['options']=OptionSerializer(vote.option.poll.option_set.all(),many=True).data
        context['log']=log
        return JsonResponse(context)
