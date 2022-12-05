# from .repo import ProductRepo
# from .serializers import ProductSerializer
import json
from accounting.views import get_invoice_context, get_product_context

from authentication.forms import AddMembershipRequestForm
from core.enums import ParameterNameEnum
from core.repo import ParameterRepo, PictureRepo
from core.views import CoreContext, MessageView, PageContext, SearchForm
# Create your views here.
from django.shortcuts import render, reverse
# Create your views here.
from django.views import View

from market.apps import APP_NAME
from market.enums import CustomerLevelEnum, ParameterMarketEnum
from market.forms import *
from market.repo import (BrandRepo, CartLineRepo, CategoryRepo, CustomerRepo, MarketInvoiceRepo, ProductRepo, ShopRepo,
                         SupplierRepo)
from market.serializers import (BrandSerializer, CartLineSerializer,
                                CategorySerializer, CustomerSerializer, ProductSerializer,ProductSpecificationSerializer, ShopSerializer,
                                SupplierSerializer)
from utility.log import leolog

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
    sidebar_categories=CategoryRepo(request=request).list_home()
    context['sidebar_categories']=sidebar_categories
    sidebar_brands=BrandRepo(request=request).list()
    context['sidebar_brands']=sidebar_brands

    me_customer=CustomerRepo(request=request).me
    context['me_customer']=me_customer
 
    me_supplier=SupplierRepo(request=request).me
    context['me_supplier']=me_supplier
    
    context['body_class'] = "ecommerce-page"
    return context

def get_customer_context(request,*args, **kwargs):
    context={}
    cart_lines=CartLineRepo(request=request).my_lines()
    context['cart_lines']=cart_lines
    context['cart_lines_s']=json.dumps(CartLineSerializer(cart_lines,many=True).data)
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
        categories = CategoryRepo(request=request).list_home()
        context['categories'] = categories
        categories_s = json.dumps(CategorySerializer(categories,many=True).data)

        # print(10*" # ")
        # print("categories_s")
        # print(categories[0].get_market_absolute_url())
        # print(categories_s)

        context['categories_s'] = categories_s
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
            pass
            # context['add_category_form'] = AddCategoryForm()

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
            pass
            # context['add_existing_product_to_category_form']=AddExistingProductToCategoryForm()

        return render(request, TEMPLATE_ROOT+"category.html", context)


class InvoicesView(View):
    def get(self, request, *args, **kwargs):
        pass


class InvoiceView(View):
    def get(self,request,*args, **kwargs):
        context=getContext(request=request)
        invoice=MarketInvoiceRepo(request=request).market_invoice(*args, **kwargs)
        
        context['COEF_PRICE']=1
        if invoice is None:
            mv=MessageView(request=request)
            mv.title="چنین فاکتوری یافت نشد."
            return mv.response()
        context.update(get_invoice_context(request=request,*args, **kwargs))
        # context['no_navbar']=True
        # context['no_footer']=True

    
        if request.user.has_perm('warehouse.add_warehousesheet'):
            from warehouse.enums import WareHouseSheetDirectionEnum
            from warehouse.repo import WareHouseSheetRepo,WareHouseRepo
            from warehouse.forms import AddWarehouseSheetForm,AddWarehouseSheetsForInvoiceForm
            context['add_ware_house_sheet_form']=AddWarehouseSheetsForInvoiceForm()
            ware_houses=WareHouseRepo(request=request).list()
            context['directions']=(direction[0] for direction in WareHouseSheetDirectionEnum.choices)
            context['ware_houses']=ware_houses
        context['LAYOUT_PARENT']="phoenix/layout.html"
        return render(request,TEMPLATE_ROOT+"market-invoice.html",context)


class CartView(View):
    def get(self, request, *args, **kwargs):
        context = getContext(request)
        if 'customer_id' in kwargs:
            customer=CustomerRepo(request=request).customer(*args, **kwargs)
        else:
            customer=CustomerRepo(request=request).me
        if customer is None:
            mv=MessageView(request=request)
            return mv.response()
        

        context['customer'] = customer
        cart_lines=customer.cartline_set.all()
        cart_lines_s = json.dumps(CartLineSerializer(cart_lines,many=True).data)
        context['cart_lines_s'] = cart_lines_s
        context['cart_lines'] = cart_lines
        context['body_class'] = "shopping-cart"
        context['shop_header_image'] = "ecommerce-page"
        
        return render(request, TEMPLATE_ROOT+"cart.html", context)


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


class CustomersView(View):
    def get(self, request, *args, **kwargs):
        context = getContext(request)
        customer_repo=CustomerRepo(request=request)
        customers=customer_repo.list(*args,**kwargs)
         

        context['customers'] = customers
        customers_s = json.dumps(CustomerSerializer(customers,many=True).data)
        context['customers_s'] = customers_s
        context['body_class'] = "ecommerce-page"
        if request.user.has_perm(APP_NAME+".add_brand"):
            context['add_brand_form'] = AddBrandForm()

        return render(request, TEMPLATE_ROOT+"customers.html", context)


class CustomerView(View):
    def get(self, request, *args, **kwargs):
        context = getContext(request)
        customer_repo=CustomerRepo(request=request)
        customer=customer_repo.customer(*args,**kwargs)
         

        context['customer'] = customer
        market_invoices=MarketInvoiceRepo(request=request).list(customer_id=customer.id)
        context['market_invoices'] = market_invoices
         
        context['body_class'] = "product-page"
        if request.user.has_perm(APP_NAME+".add_brand"):
            context['add_brand_form'] = AddBrandForm()

        return render(request, TEMPLATE_ROOT+"customer.html", context)


class ShopsView(View):
    def get(self, request, *args, **kwargs):
        context = getContext(request)
        shop_repo=ShopRepo(request=request)
        shops=shop_repo.list(*args,**kwargs)
         

        context['shops'] = shops
        shops_s = json.dumps(ShopSerializer(shops,many=True).data)
        context['shops_s'] = shops_s
        context['body_class'] = "ecommerce-page"
        if request.user.has_perm(APP_NAME+".add_brand"):
            context['add_brand_form'] = AddBrandForm()

        return render(request, TEMPLATE_ROOT+"shops.html", context)


class ShopView(View):
    def get(self, request, *args, **kwargs):
        context = getContext(request)
        shop_repo=ShopRepo(request=request)
        shop=shop_repo.shop(*args,**kwargs)
        if shop is None:
            mv=MessageView(request=request)
            return mv.response()
        

        context['shop'] = shop
        shop_s = json.dumps(ShopSerializer(shop).data)
        context['shop_s'] = shop_s 
        context['body_class'] = "ecommerce-page"
        context['shop_header_image'] = "ecommerce-page"
        
        context.update(PageContext(request=request,page=shop.product_or_service))

        return render(request, TEMPLATE_ROOT+"shop.html", context)


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
        search_form=SearchForm(request.POST)
        if search_form.is_valid():
            search_for=search_form.cleaned_data['search_for']
            products=ProductRepo(request=request).list(search_for=search_for)
            context['products']=products
            products_s=json.dumps(ProductSerializer(products,many=True).data)
            context['products_s']=products_s
            return render(request,TEMPLATE_ROOT+"search.html",context)


class ProductView(View):
    def get(self,request,*args, **kwargs):
        context=getContext(request=request)
        product=ProductRepo(request=request).product(*args, **kwargs)
        context.update(PageContext(request=request,page=product))
        context.update(get_product_context(request=request,product=product))
        context['product']=product
        context['body_class']="product-page"
        product_s=json.dumps(ProductSerializer(product).data)
        context['product_s']=product_s
        from core.serializers import PageImageSerializer
        images=product.pageimage_set.all()
        images_s=json.dumps(PageImageSerializer(images,many=True).data)
        context['images_s']=images_s
        related_pages_=product.related_pages.filter(class_name="product")
        ids=(p.id for p in related_pages_)
        related_pages=ProductRepo(request=request).list().filter(id__in=ids)
        related_pages_s=json.dumps(ProductSerializer(related_pages,many=True).data)
        context['related_pages_s']=related_pages_s
        context['related_pages']=related_pages

        # shops=product.shop_set.all()
        # shops_s=json.dumps(ShopSerializer(shops,many=True).data)
        # context["shops_s"]=shops_s


        me_supplier=context["me_supplier"]
        me_customer=context["me_customer"]
        
        if me_supplier is not None:
            supplier_shops=ShopRepo(request=request).list(product_id=product.id,supplier_id=me_supplier.id)
            context['add_shop_form']=AddShopForm()
            context['shop_levels'] = (i[0] for i in CustomerLevelEnum.choices)
            shops=ShopRepo(request=request).list(product_id=product.id,supplier_id=me_supplier.id)
            shops_s=json.dumps(ShopSerializer(shops,many=True).data)
            context["supplier_shops_s"]=shops_s
            context["supplier_shops"]=shops
        else:
            supplier_shops=[]
        
        if me_customer is not None:
            in_cart,in_cart_unit=CartLineRepo(request=request).in_cart(product_or_service_id=product.pk,customer_id=me_customer.pk)
            context.update(get_customer_context(request=request,customer=me_customer))
            context['in_cart']=in_cart
            context['in_cart_unit']=in_cart_unit
            shops=ShopRepo(request=request).list(product_id=product.id,level=me_customer.level)
            shops_s=json.dumps(ShopSerializer(shops,many=True).data)
            context["customer_shops_s"]=shops_s
            context["customer_shops"]=shops
        return render(request,TEMPLATE_ROOT+"product.html",context)
