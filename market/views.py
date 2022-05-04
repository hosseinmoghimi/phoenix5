from django.shortcuts import render
from core.enums import ParameterNameEnum
from market.enums import ParameterMarketEnum
from market.repo import SupplierRepo
from market.serializers import SupplierSerializer
from market.forms import *
from authentication.forms import AddMembershipRequestForm
from core.repo import ParameterRepo, PictureRepo
from .repo import CategoryRepo, ProductRepo
from .serializers import CategorySerializer, ProductSerializer
# Create your views here.
from django.shortcuts import render,reverse
from core.views import CoreContext,SearchForm
# Create your views here.
from django.views import View
from .apps import APP_NAME
from accounting.forms import AddProductForm
# from .repo import ProductRepo
# from .serializers import ProductSerializer
import json
 

TEMPLATE_ROOT = "market/"
LAYOUT_PARENT = "material-kit-pro/layout.html"


def getContext(request, *args, **kwargs):
    context = CoreContext(request=request, app_name=APP_NAME)
    context['search_form'] = SearchForm()
    context['search_action'] = reverse(APP_NAME+":search")
    context['LAYOUT_PARENT'] = LAYOUT_PARENT
    return context


class HomeView(View):
    def get(self, request, *args, **kwargs):
        context = getContext(request)
        context['body_class'] = "ecommerce-page"
        parameter_repo = ParameterRepo(request=request, app_name=APP_NAME)
        context['shop_header_title'] = parameter_repo.parameter(
            name=ParameterMarketEnum.SHOP_HEADER_TITLE)
        context['shop_header_slogan'] = parameter_repo.parameter(
            name=ParameterMarketEnum.SHOP_HEADER_SLOGAN)
        context['shop_header_image'] = PictureRepo(
            request=request, app_name=APP_NAME).picture(name=ParameterMarketEnum.SHOP_HEADER_IMAGE)
        categories = CategoryRepo(request=request).list().exclude(parent_id__gte=1)
        context['categories'] = categories
        context['categories_s'] = json.dumps(CategorySerializer(categories,many=True).data)
        # context['offers'] = OfferRepo(request=request).list(for_home=True)
        # context['blogs'] = BlogRepo(request=request).list(for_home=True)
        products = ProductRepo(request=request).objects.filter(pk=0)
        context['products'] = products
        context['products_s'] = json.dumps(ProductSerializer(products,many=True).data)
        # context['top_products'] = products.order_by('-priority')[:3]
        if request.user.has_perm(APP_NAME+".add_product") and len(categories) == 0:
            context['add_product_form'] = AddProductForm()
        if request.user.has_perm(APP_NAME+".add_category") and len(products) == 0:
            context['add_category_form'] = AddCategoryFrom()

        context['add_membership_request_form'] = AddMembershipRequestForm()


        #suppliers
        if True:
            suppliers = SupplierRepo(request=request).list()
            context['suppliers'] = suppliers
            context['suppliers_s'] = json.dumps(SupplierSerializer(suppliers,many=True).data)

        return render(request, TEMPLATE_ROOT+"index.html", context)

class CategoryView(View):
    def get(self, request, *args, **kwargs):
        context = getContext(request)
        context['body_class'] = "ecommerce-page"
        parameter_repo = ParameterRepo(request=request, app_name=APP_NAME)
        category=CategoryRepo(request=request).category(*args, **kwargs)
        context['category']=category
        context['shop_header_title'] = parameter_repo.parameter(
            name=ParameterMarketEnum.SHOP_HEADER_TITLE)
        context['shop_header_slogan'] = parameter_repo.parameter(
            name=ParameterMarketEnum.SHOP_HEADER_SLOGAN)
        context['shop_header_image'] = PictureRepo(
            request=request, app_name=APP_NAME).picture(name=ParameterMarketEnum.SHOP_HEADER_IMAGE)
        categories = category.childs.all()
        context['categories'] = categories
        context['categories_s'] = json.dumps(CategorySerializer(categories,many=True).data)
        # context['offers'] = OfferRepo(request=request).list(for_home=True)
        # context['blogs'] = BlogRepo(request=request).list(for_home=True)
        products = category.products.all()
        context['products'] = products
        context['products_s'] = json.dumps(ProductSerializer(products,many=True).data)
        # context['top_products'] = products.order_by('-priority')[:3]
        if request.user.has_perm(APP_NAME+".add_product") and len(categories) == 0:
            context['add_product_form'] = AddProductForm()
        if request.user.has_perm(APP_NAME+".add_category") and len(products) == 0:
            context['add_category_form'] = AddCategoryFrom()

        context['add_membership_request_form'] = AddMembershipRequestForm()

        return render(request, TEMPLATE_ROOT+"category.html", context)

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

class ProductView(View):
    def get(self,request,*args, **kwargs):
        context=getContext(request=request)
        products=ProductRepo(request=request).list()
        context['products']=products
        products_s=json.dumps(ProductSerializer(products,many=True).data)
        context['products_s']=products_s
        return render(request,TEMPLATE_ROOT+"product.html",context)