from django.shortcuts import render
# Create your views here.
from django.shortcuts import render,reverse
from core.views import CoreContext,SearchForm
# Create your views here.
from django.views import View
from core.repo import ParameterRepo
from .enums import ParameterNameEnum
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
    context['office_address']=param_repo.parameter(name=ParameterNameEnum.OFFICE_ADDRESS).value
    context['office_tel']=param_repo.parameter(name=ParameterNameEnum.OFFICE_TEL).value
    context['office_email']=param_repo.parameter(name=ParameterNameEnum.OFFICE_EMAIL).value
    context['office_mobile']=param_repo.parameter(name=ParameterNameEnum.OFFICE_MOBILE).value
   
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
        
        return render(request,TEMPLATE_ROOT+"index.html",context)

class SearchView(View):
    def get(self,request,*args, **kwargs):
        context=getContext(request=request)
        products=ProductRepo(request=request).list()
        context['products']=products
        products_s=json.dumps(ProductSerializer(products,many=True).data)
        context['products_s']=products_s
        return render(request,TEMPLATE_ROOT+"index.html",context)
    def post(self,request,*args, **kwargs):
        context=getContext(request=request)
        products=ProductRepo(request=request).list()
        context['products']=products
        products_s=json.dumps(ProductSerializer(products,many=True).data)
        context['products_s']=products_s
        return render(request,TEMPLATE_ROOT+"index.html",context)
