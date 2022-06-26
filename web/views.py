from django.shortcuts import render
# Create your views here.
from django.shortcuts import render,reverse
from core.views import CoreContext, PageContext,SearchForm
# Create your views here.
from django.views import View
from core.repo import ParameterRepo, PictureRepo
from .enums import ParameterEnum, ParameterNameEnum, PictureNamesEnum
from .apps import APP_NAME
# from .repo import ProductRepo
# from .serializers import ProductSerializer
import json
from .repo import BlogRepo,FeatureRepo, OurTeamRepo,OurWorkRepo,CarouselRepo, PricingItemRepo, PricingPageRepo, TestimonialRepo

TEMPLATE_ROOT = "web/"
LAYOUT_PARENT = "material-kit-pro/layout.html"


def getContext(request, *args, **kwargs):
    context = CoreContext(request=request, app_name=APP_NAME)
    context['search_form'] = SearchForm()
    context['search_action'] = reverse(APP_NAME+":search")
    context['LAYOUT_PARENT'] = LAYOUT_PARENT

    if 'profile' in context and False:
        profile=context['profile']
        context['profile_button']={}
        context['profile_button']['url']=profile.get_absolute_url()
        context['profile_button']['color']="rose"
        context['profile_button']['title']=profile.name
        context['profile_button']['image']=profile.image
        context['profile_button']['icon']=""

 

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

    picture_repo=PictureRepo(request=request,app_name=APP_NAME)
    context['contact_us_back_img']=picture_repo.picture(name=PictureNamesEnum.CONTACT_US,default="web/img/contact-us.jpg")
   
    return context
class HomeView(View):
    def get(self,request,*args, **kwargs):
        context=getContext(request=request)
        context.update(get_contact_us_context(request=request))


        carousels=CarouselRepo(request=request).list()
        context['carousels']=carousels


        features=FeatureRepo(request=request).list(for_home=True)
        context['features']=features
        


        blogs=BlogRepo(request=request).list(for_home=True,*args, **kwargs)
        context['blogs']=blogs

        our_works=OurWorkRepo(request=request).list(for_home=True)
        context['our_works']=our_works
        


        our_works=OurWorkRepo(request=request).list(for_home=True,*args, **kwargs)
        context['our_works']=our_works

        our_teams=OurTeamRepo(request=request).list(for_home=True,*args, **kwargs)
        context['our_teams']=our_teams

        testimonials=TestimonialRepo(request=request).list(*args, **kwargs)
        context['testimonials']=testimonials

        pricing_pages=PricingPageRepo(request=request).list()
        context['pricing_pages']=pricing_pages



        parameter_repo=ParameterRepo(request=request,app_name=APP_NAME)
        
        context['blog_title_param']=parameter_repo.parameter(name=ParameterEnum.BLOGS_TITLE)
        context['blog_description_param']=parameter_repo.parameter(name=ParameterEnum.BLOGS_DESCRIPTION)

        context['feature_title_param']=parameter_repo.parameter(name=ParameterEnum.FEATURES_TITLE)
        context['feature_description_param']=parameter_repo.parameter(name=ParameterEnum.FEATURES_DESCRIPTION)
        
        context['ourwork_pretitle_param']=parameter_repo.parameter(name=ParameterEnum.OUR_WORKS_PRE_TITLE)
        context['ourwork_title_param']=parameter_repo.parameter(name=ParameterEnum.OUR_WORKS_TITLE)
        context['ourwork_description_param']=parameter_repo.parameter(name=ParameterEnum.OUR_WORKS_DESCRIPTION)

        context['ourteam_title_param']=parameter_repo.parameter(name=ParameterEnum.OUR_TEAMS_TITLE)
        context['ourteam_description_param']=parameter_repo.parameter(name=ParameterEnum.OUR_TEAMS_DESCRIPTION)

        context['testimonial_title_param']=parameter_repo.parameter(name=ParameterEnum.TESTIMONIAL_TITLE)

        
        context['pricing_title_param']=parameter_repo.parameter(name=ParameterEnum.PRICING_TITLE)

        
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


class PricingPageView(View):
    def get(self,request,*args, **kwargs):
        context=getContext(request=request)
        pricing_page=PricingPageRepo(request=request).pricing_page(*args, **kwargs)
        context['pricing_page']=pricing_page
        context.update(PageContext(request=request,page=pricing_page))
        context['body_class']="pricing sidebar-collapse"
        return render(request,TEMPLATE_ROOT+"pricing-page.html",context)
class PricingItemView(View):
    def get(self,request,*args, **kwargs):
        context=getContext(request=request)
        pricing_item=PricingItemRepo(request=request).pricing_item(*args, **kwargs)
        context['body_class']="pricing sidebar-collapse"
        return render(request,TEMPLATE_ROOT+"pricing-item.html",context)

class BlogView(View):
    def get(self,request,*args, **kwargs):
        context=getContext(request=request)
        blog=BlogRepo(request=request).blog(*args, **kwargs)
        context.update(PageContext(request=request,page=blog))
        return render(request,TEMPLATE_ROOT+"blog.html",context)
class FeatureView(View):
    def get(self,request,*args, **kwargs):
        context=getContext(request=request)
        feature=FeatureRepo(request=request).feature(*args, **kwargs)
        context.update(PageContext(request=request,page=feature))
        return render(request,TEMPLATE_ROOT+"feature.html",context)
class OurTeamView(View):
    def get(self,request,*args, **kwargs):
        context=getContext(request=request)
        context['body_class']="profile-page"
        our_team=OurTeamRepo(request=request).our_team(*args, **kwargs)
        context['our_team']=our_team
        return render(request,TEMPLATE_ROOT+"our-team.html",context)
class OurWorkView(View):
    def get(self,request,*args, **kwargs):
        context=getContext(request=request)
        our_work=OurWorkRepo(request=request).our_work(*args, **kwargs)
        context.update(PageContext(request=request,page=our_work))
        return render(request,TEMPLATE_ROOT+"our-work.html",context)