from rest_framework.views import APIView
from .forms import *
from .repo import GroupRepo,FAILED,SUCCEED,SalaryRepo
from .serializers import GroupSerializer,SalarySerializer
from django.http import JsonResponse

class AddGroupApi(APIView):
    def post(self,request,*args, **kwargs):
        message=""
        result=FAILED
        context={}
        if request.method=='POST':
            log=2
            AddGroupForm_=AddGroupForm(request.POST)
            if AddGroupForm_.is_valid():
                cd=AddGroupForm_.cleaned_data
                result,message,group=GroupRepo(request=request).add_group(**cd)
                if result==SUCCEED:
                    context['group']=GroupSerializer(group).data
        context['result']=result
        context['message']=message
        context['log']=log
        return JsonResponse(context)



class AddSalaryApi(APIView):
    def post(self,request,*args, **kwargs):
        message=""
        result=FAILED
        context={}
        if request.method=='POST':
            log=2
            AddSalaryForm_=AddSalaryForm(request.POST)
            if AddSalaryForm_.is_valid():
                cd=AddSalaryForm_.cleaned_data
                result,message,salary=SalaryRepo(request=request).add_salary(**cd)
                if result==SUCCEED:
                    context['salary']=SalarySerializer(salary).data
        context['result']=result
        context['message']=message
        context['log']=log
        return JsonResponse(context)


