from django.shortcuts import render
from core.enums import ParameterNameEnum
from market.enums import ParameterMarketEnum
from market.repo import BrandRepo, SupplierRepo,CartLineRepo
from market.serializers import BrandSerializer, SupplierSerializer,CartLineSerializer
from market.forms import *
from authentication.forms import AddMembershipRequestForm
from core.repo import ParameterRepo, PictureRepo
from market.repo import CategoryRepo, ProductRepo
from market.serializers import CategorySerializer, ProductSerializer
# Create your views here.
from django.shortcuts import render,reverse
from core.views import CoreContext, MessageView, PageContext,SearchForm
# Create your views here.
from django.views import View
from market.apps import APP_NAME
# from .repo import ProductRepo
# from .serializers import ProductSerializer
import json
 

TEMPLATE_ROOT = "market/"

LAYOUT_PARENT = "phoenix/layout.html"
LAYOUT_PARENT = "material-kit-pro/layout.html"
WIDE_LAYOUT_PARENT = "phoenix/wide-layout.html"
WIDE_LAYOUT_PARENT = "material-kit-pro/layout.html"


def getContext(request, *args, **kwargs):
    context = CoreContext(request=request, app_name=APP_NAME)
    context['search_form'] = SearchForm()
    context['search_action'] = reverse(APP_NAME+":search")
    context['LAYOUT_PARENT'] = LAYOUT_PARENT
    context['WIDE_LAYOUT_PARENT'] = WIDE_LAYOUT_PARENT
    sidebar_categories=CategoryRepo(request=request).list(parent_id=None)
    context['sidebar_categories']=sidebar_categories
    sidebar_brands=BrandRepo(request=request).list()
    context['sidebar_brands']=sidebar_brands
    return context

def get_customer_context(request,*args, **kwargs):
    context={}
    cart_lines=CartLineRepo(request=request).my_lines()
    context['cart_lines']=cart_lines
    context['cart_lines_s']=json.dumps(CartLineSerializer(cart_lines).data)
    return context


def get_suppliers_context(request,*args, **kwargs):
    context={}
    suppliers=SupplierRepo(request=request).list()
    sidebar_suppliers=SupplierRepo(request=request).list().order_by('priority')[:5]
    context['sidebar_suppliers']=sidebar_suppliers
    context['suppliers']=suppliers
    context['suppliers_s']=json.dumps(SupplierSerializer(suppliers,many=True).data)
    return context
class SupplierView(View):
    def get(self, request, *args, **kwargs):
        context = getContext(request)
        context['body_class'] = "ecommerce-page"

        context.update(get_customer_context(request=request,*args, **kwargs))
        context.update(get_suppliers_context(request=request,*args, **kwargs))
        supplier=SupplierRepo(request=request).supplier(*args, **kwargs)
        context['supplier']=supplier
        shop_header_image={
            'image':supplier.header
        }
        context['shop_header_image']=shop_header_image


        return render(request, TEMPLATE_ROOT+"supplier.html", context)

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
        category=None
        context['category_s'] = json.dumps(CategorySerializer(category).data)
        # context['offers'] = OfferRepo(request=request).list(for_home=True)
        # context['blogs'] = BlogRepo(request=request).list(for_home=True)
        products = ProductRepo(request=request).objects.filter(pk=0)
        context['products'] = products
        context['products_s'] = json.dumps(ProductSerializer(products,many=True).data)
        # context['top_products'] = products.order_by('-priority')[:3]
        # if request.user.has_perm("core.add_product") and len(categories) == 0:
        if request.user.has_perm("core.add_product"):
            context['add_product_form'] = AddProductForm()
        # if request.user.has_perm(APP_NAME+".add_category") and len(products) == 0:
        if request.user.has_perm(APP_NAME+".add_category"):
            context['add_category_form'] = AddCategoryForm()

        context['add_membership_request_form'] = AddMembershipRequestForm()

 

        if True:
            context['parent_s']=json.dumps(CategorySerializer(None).data)


        context.update(get_customer_context(request=request,*args, **kwargs))
        context.update(get_suppliers_context(request=request,*args, **kwargs))

        return render(request, TEMPLATE_ROOT+"shop.html", context)

class CategoryView(View):
    def get(self, request, *args, **kwargs):
        context = getContext(request)
        category_repo=CategoryRepo(request=request)
        category=category_repo.category(*args,**kwargs)
        if category is None:
            mv=MessageView(request=request)
            return mv.response()
        context.update(get_customer_context(request=request,*args, **kwargs))
        context.update(get_suppliers_context(request=request,*args, **kwargs))
        

        context['category'] = category
        category_s = json.dumps(CategorySerializer(category).data)
        context['category_s'] = category_s
        context['parent_s']=category_s
        context['parent']=category
        context['body_class'] = "ecommerce-page"
        parameter_repo = ParameterRepo(request=request, app_name=APP_NAME)
        context['shop_header_title'] = parameter_repo.parameter(
            name=ParameterMarketEnum.SHOP_HEADER_TITLE)
        context['shop_header_slogan'] = parameter_repo.parameter(
            name=ParameterMarketEnum.SHOP_HEADER_SLOGAN)
        context['shop_header_image'] = PictureRepo(
            request=request, app_name=APP_NAME).picture(name=ParameterMarketEnum.SHOP_HEADER_IMAGE)
        categories = category_repo.list(parent_id=category.id)
        context['categories'] = categories
        context['categories_s'] = json.dumps(CategorySerializer(categories,many=True).data)
        # context['offers'] = OfferRepo(request=request).list(for_home=True)
        # context['blogs'] = BlogRepo(request=request).list(for_home=True)
        products = category.products.all()
        context['products'] = products
        context['products_s'] = json.dumps(ProductSerializer(products,many=True).data)
        # context['top_products'] = products.order_by('-priority')[:3]
        # if request.user.has_perm("core.add_product") and len(categories) == 0:
        if request.user.has_perm("accounting.add_product"):
            context['add_product_form'] = AddProductForm()
        # if request.user.has_perm(APP_NAME+".add_category") and len(products) == 0:
        if request.user.has_perm(APP_NAME+".add_category"):
            context['add_category_form'] = AddCategoryForm()

        context['add_membership_request_form'] = AddMembershipRequestForm()

        if request.user.has_perm(APP_NAME+".change_category"):
            context['add_existing_product_to_category_form']=AddExistingProductToCategoryForm()

        return render(request, TEMPLATE_ROOT+"category.html", context)



class BrandsView(View):
    def get(self, request, *args, **kwargs):
        context = getContext(request)
        brand_repo=BrandRepo(request=request)
        brands=brand_repo.category(*args,**kwargs)
         

        context['brands'] = brands
        brands_s = json.dumps(BrandSerializer(brands,many=True).data)
        context['brands_s'] = brands_s
        context['body_class'] = "ecommerce-page"
        if request.user.has_perm(APP_NAME+".add_brand"):
            context['add_brand_form'] = AddBrandForm()



       

        return render(request, TEMPLATE_ROOT+"brands.html", context)



class BrandView(View):
    def get(self, request, *args, **kwargs):
        context = getContext(request)
        brand_repo=BrandRepo(request=request)
        brand=brand_repo.brand(*args,**kwargs)
        if brand is None:
            mv=MessageView(request=request)
            return mv.response()
        

        context['brand'] = brand
        brand_s = json.dumps(BrandSerializer(brand).data)
        context['brand_s'] = brand_s
        products=brand.products.all()
        context['products'] = products
        products_s = json.dumps(ProductSerializer(products,many=True).data)
        context['products_s'] = products_s
        context['body_class'] = "ecommerce-page"
        context['shop_header_image'] = "ecommerce-page"
        
        context.update(PageContext(request=request,page=brand))

       

        return render(request, TEMPLATE_ROOT+"brand.html", context)


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