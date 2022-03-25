from django.shortcuts import render
# Create your views here.
from django.shortcuts import render,reverse
from core.views import CoreContext,SearchForm
# Create your views here.
from django.views import View
from core.repo import ParameterRepo
from .enums import ParameterEnum, ParameterNameEnum
from .apps import APP_NAME
# from .repo import ProductRepo
# from .serializers import ProductSerializer
import json
from .repo import BlogRepo,FeatureRepo,OurWorkRepo,CarouselRepo

TEMPLATE_ROOT = "web/"
LAYOUT_PARENT = "material-kit-pro/layout.html"


def getContext(request, *args, **kwargs):
    context = CoreContext(request=request, app_name=APP_NAME)
    context['search_form'] = SearchForm()
    context['search_action'] = reverse(APP_NAME+":search")
    context['LAYOUT_PARENT'] = LAYOUT_PARENT
    return context


def get_contact_us_context(request):
    context={}
    param_repo=ParameterRepo(request=request,app_name=APP_NAME)
    context['office_address']=param_repo.parameter(name=ParameterNameEnum.OFFICE_ADDRESS)
    context['office_tel']=param_repo.parameter(name=ParameterNameEnum.OFFICE_TEL)
    context['office_email']=param_repo.parameter(name=ParameterNameEnum.OFFICE_EMAIL)
    context['office_mobile']=param_repo.parameter(name=ParameterNameEnum.OFFICE_MOBILE)
    context['contact_us_description']=param_repo.parameter(name=ParameterEnum.CONTACT_US_TITLE,default="""در صورت نیاز با اطلاعات بیشتر در مورد نحوه استفاده از اپلیکیشن ها از طریق راه های ارتباطی زیر میتوانید با ما در ارتباط باشید.""")
    context['contact_us_title']=param_repo.parameter(name=ParameterEnum.CONTACT_US_DESCRIPTION,default="""با ما در ارتباط باشید""")

   
    return context
class HomeView(View):
    def get(self,request,*args, **kwargs):
        context=getContext(request=request)
        context.update(get_contact_us_context(request=request))
        blogs=BlogRepo(request=request).list()
        context['blogs']=blogs

        features=FeatureRepo(request=request).list()
        context['features']=features
        

        our_works=OurWorkRepo(request=request).list()
        context['our_works']=our_works
        

        carousels=CarouselRepo(request=request).list()
        context['carousels']=carousels




        parameter_repo=ParameterRepo(request=request,app_name=APP_NAME)
        
        context['blog_title_param']=parameter_repo.parameter(name=ParameterEnum.BLOGS_TITLE)
        context['blog_description_param']=parameter_repo.parameter(name=ParameterEnum.BLOGS_DESCRIPTION)

        context['feature_title_param']=parameter_repo.parameter(name=ParameterEnum.FEATURES_TITLE)
        context['feature_description_param']=parameter_repo.parameter(name=ParameterEnum.FEATURES_DESCRIPTION)
        
        context['ourwork_pretitle_param']=parameter_repo.parameter(name=ParameterEnum.OUR_WORKS_PRE_TITLE)
        context['ourwork_title_param']=parameter_repo.parameter(name=ParameterEnum.OUR_WORKS_TITLE)
        context['ourwork_description_param']=parameter_repo.parameter(name=ParameterEnum.OUR_WORKS_DESCRIPTION)

        context['ourteam_title_param']=parameter_repo.parameter(name=ParameterEnum.OUR_WORKS_TITLE)
        context['ourteam_description_param']=parameter_repo.parameter(name=ParameterEnum.OUR_TEAMS_DESCRIPTION)

        context['testimonial_title_param']=parameter_repo.parameter(name=ParameterEnum.TESTIMONIAL_TITLE)

        
        return render(request,TEMPLATE_ROOT+"index.html",context)

class SearchView(View):
    def get(self,request,*args, **kwargs):
        context=getContext(request=request)
        blogs=BlogRepo(request=request).list()
        context['blogs']=blogs
        return render(request,TEMPLATE_ROOT+"search.html",context)
    def post(self,request,*args, **kwargs):
        context=getContext(request=request)
        search_form=SearchForm(request.POST)
        if search_form.is_valid():
            search_for=search_form.cleaned_data.get('search_for')
            context['search_for']=search_for

            blogs=BlogRepo(request=request).list(search_for=search_for)
            context['blogs']=blogs

            features=FeatureRepo(request=request).list(search_for=search_for)
            context['features']=features

            our_works=OurWorkRepo(request=request).list(search_for=search_for)
            context['our_works']=our_works

        return render(request,TEMPLATE_ROOT+"search.html",context) 
