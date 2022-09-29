from accounting.repo import AccountRepo, ProductRepo as ProductRepo_origin,CategoryRepo
from market.apps import APP_NAME
from market.models import Brand, Cart, CartLine, Category, Customer, Shop, Supplier
from django.db.models import Q
from authentication.repo import ProfileRepo



class ProductRepo(ProductRepo_origin): 
    def list(self,*args, **kwargs):
        objects=self.objects
        if 'category_id' in kwargs:
            category=Category.objects.get(pk=kwargs['category_id'])
            if category is not None:
                return category.products.order_by('priority')

        if 'for_home' in kwargs:
            hps=objects=HomeProducts.objects.all()
            objects = objects.filter(Q(for_home=kwargs['for_home']))
        if 'search_for' in kwargs:
            return objects.filter(Q(title__contains=kwargs['search_for'])|Q(short_description__contains=kwargs['search_for']))
        return objects

class CategoryRepo121():  
    def __init__(self, *args, **kwargs):
        self.request = None
        self.user = None
        if 'request' in kwargs:
            self.request = kwargs['request']
            self.user = self.request.user
        if 'user' in kwargs:
            self.user = kwargs['user']
        
        self.objects=Category.objects.all()
        self.profile=ProfileRepo(*args, **kwargs).me
       

    def category(self, *args, **kwargs):
        pk=0
        if 'category_id' in kwargs:
            pk= kwargs['category_id']
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
            parent_id=kwargs['parent_id']
            if parent_id is None:
                objects=objects.filter(parent=None)
            else:
                objects=objects.filter(parent_id=kwargs['parent_id'])
        return objects.all()

    def add_category(self,*args, **kwargs):
        if not self.user.has_perm(APP_NAME+".add_category"):
            return None
        parent_id=None
        category=Category()
        if 'title' in kwargs:
            category.title = kwargs['title']
            
        if 'parent_id' in kwargs:
            parent_id = kwargs['parent_id']
            if parent_id is not None and parent_id!=0:
                category.parent_id=parent_id

        category.save()
        return category



class BrandRepo():  
    def __init__(self, *args, **kwargs):
        self.request = None
        self.user = None
        if 'request' in kwargs:
            self.request = kwargs['request']
            self.user = self.request.user
        if 'user' in kwargs:
            self.user = kwargs['user']
        
        self.objects=Brand.objects.all()
        self.profile=ProfileRepo(*args, **kwargs).me
       

    def brand(self, *args, **kwargs):
        pk=0
        if 'brand_id' in kwargs:
            pk= kwargs['brand_id']
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
        # if 'for_home' in kwargs:
        #     objects = objects.filter(Q(for_home=kwargs['for_home']))
         
        return objects.all()

    def add_brand(self,*args, **kwargs):
        if not self.user.has_perm(APP_NAME+".add_brand"):
            return None
        parent_id=None
        brand=Brand()
        if 'title' in kwargs:
            brand.title = kwargs['title']
            
        if 'parent_id' in kwargs:
            parent_id = kwargs['parent_id']
            if parent_id is not None and parent_id!=0:
                brand.parent_id=parent_id

        brand.save()
        return brand


        
class SupplierRepo():  
    def __init__(self, *args, **kwargs):
        self.request = None
        self.user = None
        if 'request' in kwargs:
            self.request = kwargs['request']
            self.user = self.request.user
        if 'user' in kwargs:
            self.user = kwargs['user']
        
        self.objects=Supplier.objects.all()
        self.profile=ProfileRepo(*args, **kwargs).me
        self.me=Supplier.objects.filter(account__profile_id=self.profile.id).first()       

    def supplier(self, *args, **kwargs):
        pk=0
        if 'supplier_id' in kwargs:
            pk= kwargs['supplier_id']
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

    def add_supplier(self,*args, **kwargs):
        if not self.user.has_perm(APP_NAME+".add_supplier"):
            return None
        title=None
        if 'title' in kwargs:
            title = kwargs['title'] 

        supplier=Supplier()
        supplier.title=title
        supplier.save()
        return supplier


class CustomerRepo():  
    def __init__(self, *args, **kwargs):
        self.request = None
        self.user = None
        self.me = None
        if 'request' in kwargs:
            self.request = kwargs['request']
            self.user = self.request.user
        if 'user' in kwargs:
            self.user = kwargs['user']
        
        self.objects=Customer.objects.all()
        self.profile=ProfileRepo(*args, **kwargs).me
        # self.account=AccountRepo(request=request).me
        if self.profile is not None:
            self.me=Customer.objects.filter(account__profile_id=self.profile.id).first()
       

    def customer(self, *args, **kwargs):
        pk=0
        if 'customer_id' in kwargs:
            pk= kwargs['customer_id']
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

    def add_customer(self,*args, **kwargs):
        if not self.user.has_perm(APP_NAME+".add_customer"):
            return None
        title=None
        customer=Customer()
        if 'title' in kwargs:
            customer.title = kwargs['title'] 
        if 'account_id' in kwargs:
            customer.account_id = kwargs['account_id'] 
        if 'profile_id' in kwargs:
            # profile = ProfileRepo(request=self.request).profile(pk=kwargs['profile_id'])
            account = AccountRepo(request=self.request).account(pk=kwargs['profile_id'])
            customer.account = account

        customer.save()
        return customer


class CartRepo():  
    def __init__(self, *args, **kwargs):
        self.request = None
        self.user = None
        if 'request' in kwargs:
            self.request = kwargs['request']
            self.user = self.request.user
        if 'user' in kwargs:
            self.user = kwargs['user']
        
        self.objects=Cart.objects.all()
        self.profile=ProfileRepo(*args, **kwargs).me
        self.customer= CustomerRepo(request=request).me
       

    def cart(self, *args, **kwargs):
        pk=0
        if 'cart_id' in kwargs:
            pk= kwargs['cart_id']
            return self.objects.filter(pk=pk).first()
       
        elif 'pk' in kwargs:
            pk=kwargs['pk']
            return self.objects.filter(pk=pk).first()
        elif 'id' in kwargs:
            pk=kwargs['id']
            return self.objects.filter(pk=pk).first()
     
    def lines(self, *args, **kwargs):
        return self.list(*args, **kwargs)

    def list(self, *args, **kwargs):
        objects = self.objects
        if 'search_for' in kwargs:
            search_for=kwargs['search_for']
            objects = objects.filter(Q(title__contains=search_for)|Q(short_description__contains=search_for)|Q(description__contains=search_for))
        if 'for_home' in kwargs:
            objects = objects.filter(Q(for_home=kwargs['for_home']))
        if 'parent_id' in kwargs:
            objects=objects.filter(parent_id=kwargs['parent_id'])
        if 'customer_id' in kwargs:
            objects=objects.filter(pay_to_id=kwargs['customer_id'])
        return objects.all()

    def add_supplier(self,*args, **kwargs):
        if not self.user.has_perm(APP_NAME+".add_supplier"):
            return None
        title=None
        if 'title' in kwargs:
            title = kwargs['title'] 

        supplier=Supplier()
        supplier.title=title
        supplier.save()
        return supplier


class ShopRepo():  
    def __init__(self, *args, **kwargs):
        self.request = None
        self.user = None
        if 'request' in kwargs:
            self.request = kwargs['request']
            self.user = self.request.user
        if 'user' in kwargs:
            self.user = kwargs['user']
        
        self.objects=Shop.objects.all()
        self.profile=ProfileRepo(*args, **kwargs).me
        self.customer= CustomerRepo(request=self.request).me
       

    def shop(self, *args, **kwargs):
        pk=0
        if 'shop_id' in kwargs:
            pk= kwargs['shop_id']
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
        if 'product_or_service_id' in kwargs:
            objects=objects.filter(productorservice_id=kwargs['product_or_service_id'])
        if 'productorservice_id' in kwargs:
            objects=objects.filter(productorservice_id=kwargs['productorservice_id'])
        if 'unit_name' in kwargs:
            objects=objects.filter(unit_name=kwargs['unit_name'])
        if 'product_id' in kwargs:
            objects=objects.filter(product_or_service_id=kwargs['product_id'])
        if 'supplier_id' in kwargs:
            objects=objects.filter(supplier_id=kwargs['supplier_id'])
        return objects.all()

    def add_shop(self,*args, **kwargs):
        if not self.user.has_perm(APP_NAME+".add_shop"):
            return None
        shop=Shop(*args, **kwargs)
        if 'product_or_service_id' in kwargs:
            shop.productorservice_id = kwargs['product_or_service_id'] 
        if 'productorservice_id' in kwargs:
            shop.productorservice_id = kwargs['productorservice_id'] 
        if 'supplier_id' in kwargs:
            shop.supplier_id = kwargs['unit_name'] 
        if 'supplier_id' in kwargs:
            shop.supplier_id = kwargs['supplier_id'] 
        if 'supplier' in kwargs:
            shop.supplier_id = kwargs['supplier'].id 

        shop.save()
        return shop


    

class CartLineRepo():  
    def __init__(self, *args, **kwargs):
        self.request = None
        self.user = None
        if 'request' in kwargs:
            self.request = kwargs['request']
            self.user = self.request.user
        if 'user' in kwargs:
            self.user = kwargs['user']
        
        self.objects=CartLine.objects.all()
        self.profile=ProfileRepo(*args, **kwargs).me
        self.customer= CustomerRepo(*args, **kwargs).me
       

    def cart_line(self, *args, **kwargs):
        pk=0
        if 'cart_line_id' in kwargs:
            pk= kwargs['cart_line_id']
            return self.objects.filter(pk=pk).first()
        if 'cartline_id' in kwargs:
            pk= kwargs['cartline_id']
            return self.objects.filter(pk=pk).first()
       
        elif 'pk' in kwargs:
            pk=kwargs['pk']
            return self.objects.filter(pk=pk).first()
        elif 'id' in kwargs:
            pk=kwargs['id']
            return self.objects.filter(pk=pk).first()
     
    def lines(self, *args, **kwargs):
        return self.list(*args, **kwargs)

    def my_lines(self, *args, **kwargs):
        if self.customer is not None:
            return self.list(customer_id=self.customer.id,*args, **kwargs)

    def list(self, *args, **kwargs):
        objects = self.objects
        if 'search_for' in kwargs:
            search_for=kwargs['search_for']
            objects = objects.filter(Q(title__contains=search_for)|Q(short_description__contains=search_for)|Q(description__contains=search_for))
        if 'for_home' in kwargs:
            objects = objects.filter(Q(for_home=kwargs['for_home']))
        if 'product_or_service_id' in kwargs:
            objects=objects.filter(shop__productorservice_id=kwargs['product_or_service_id'])
        if 'productorservice_id' in kwargs:
            objects=objects.filter(shop__productorservice_id=kwargs['productorservice_id'])
        if 'unit_name' in kwargs:
            objects=objects.filter(shop__unit_name=kwargs['unit_name'])
        if 'shop_id' in kwargs:
            objects=objects.filter(shop_id=kwargs['shop_id'])
        if 'customer_id' in kwargs:
            objects=objects.filter(customer_id=kwargs['customer_id'])
        return objects.all()

    def add_supplier(self,*args, **kwargs):
        if not self.user.has_perm(APP_NAME+".add_supplier"):
            return None
        title=None
        if 'title' in kwargs:
            title = kwargs['title'] 

        supplier=Supplier()
        supplier.title=title
        supplier.save()
        return supplier


        