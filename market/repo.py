from accounting.models import InvoiceLine, ProductSpecification
from accounting.repo import AccountRepo, ProductRepo as ProductRepo_origin,CategoryRepo
from core.enums import UnitNameEnum
from market.apps import APP_NAME
from market.models import Brand, Cart, CartLine, Category, Customer, MarketInvoice, Shop, Supplier
from django.db.models import Q
from authentication.repo import ProfileRepo
from phoenix.constants import FAILED, SUCCEED
from utility.log import leolog
from django.utils import timezone


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
        if self.profile is not None:
            self.me=Supplier.objects.filter(account__profile_id=self.profile.id).first()       
        else:
            self.me=None
    def supplier(self, *args, **kwargs):
        pk=0
        if 'supplier' in kwargs:
            supplier= kwargs['supplier']
            return supplier
       
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
        if 'region_id' in kwargs:
            objects=objects.filter(region_id=kwargs['region_id'])
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

  
    def add_supplier(self,*args, **kwargs):
        result=FAILED
        inviter_id=0
        message=""
        supplier=None
        if not self.request.user.has_perm(APP_NAME+".add_supplier"):
            return
        account_id=kwargs['account_id']
        region_id=kwargs['region_id']
        supplier=Customer.objects.filter(account_id=account_id).first()
        if supplier is not None:
            result=FAILED
            message="قبلا  مشتری با این اکانت ایجاد شده است."
            return result,message,supplier
        supplier=self.supplier(*args, **kwargs)
        if supplier is None:
            supplier=Supplier()
            supplier.account_id=account_id
            supplier.region_id=region_id
            if 'inviter_id' in kwargs:
                inviter_id=kwargs['inviter_id']
            if inviter_id is not None and inviter_id>0:
                supplier.inviter_id=inviter_id
            supplier.save()
        if supplier is not None:
            result=SUCCEED
            message="فروشنده جدید با موفقیت افزوده شد."
        return result,message,supplier

    

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
        if 'customer' in kwargs:
            return kwargs['customer']
       
        if 'customer_id' in kwargs:
            pk= kwargs['customer_id']
            return self.objects.filter(pk=pk).first()
       
        elif 'pk' in kwargs:
            pk=kwargs['pk']
            return self.objects.filter(pk=pk).first()
        elif 'id' in kwargs:
            pk=kwargs['id']
            return self.objects.filter(pk=pk).first()
     
    def add_customer(self,*args, **kwargs):
        result=FAILED
        message=""
        mobile=""
        customer=None
        if not self.request.user.has_perm(APP_NAME+".add_customer"):
            return
        account_id=kwargs['account_id']
        region_id=kwargs['region_id']
        if 'mobile' in kwargs:
            mobile=kwargs['mobile']
        customer=Customer.objects.filter(account_id=account_id).first()
        if customer is not None:
            result=FAILED
            message="قبلا  مشتری با این اکانت ایجاد شده است."
            return result,message,customer
        customer=self.customer(*args, **kwargs)
        if customer is None:
            customer=Customer()
            customer.account_id=account_id
            customer.region_id=region_id
            inviter_id=0
            if 'inviter_id' in kwargs:
                inviter_id=kwargs['inviter_id']
            if inviter_id is not None and inviter_id>0:
            
                customer.inviter_id=inviter_id
        
        customer.account.mobile=mobile
        if customer is not None:
            customer.save()
            customer.account.save()
            result=SUCCEED
            message="مشتری جدید با موفقیت افزوده شد."
        return result,message,customer

    
    def list(self, *args, **kwargs):
        objects = self.objects
        if 'search_for' in kwargs:
            search_for=kwargs['search_for']
            objects = objects.filter(Q(title__contains=search_for)|Q(short_description__contains=search_for)|Q(description__contains=search_for))
        if 'for_home' in kwargs:
            objects = objects.filter(Q(for_home=kwargs['for_home']))
        if 'parent_id' in kwargs:
            objects=objects.filter(parent_id=kwargs['parent_id'])
        if 'region_id' in kwargs:
            objects=objects.filter(region_id=kwargs['region_id'])
        return objects.all()



class MarketInvoiceRepo():  
    def __init__(self, *args, **kwargs):
        self.request = None
        self.user = None
        self.me = None
        if 'request' in kwargs:
            self.request = kwargs['request']
            self.user = self.request.user
        if 'user' in kwargs:
            self.user = kwargs['user']
        
        self.objects=MarketInvoice.objects.all()
        self.profile=ProfileRepo(*args, **kwargs).me
        # self.account=AccountRepo(request=request).me
        if self.profile is not None:
            self.me=Customer.objects.filter(account__profile_id=self.profile.id).first()
       

    def market_invoice(self, *args, **kwargs):
        pk=0
        if 'market_invoice_id' in kwargs:
            pk= kwargs['market_invoice_id']
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
        if 'customer_id' in kwargs:
            customer=Customer.objects.filter(pk=kwargs['customer_id']).first()
            if customer is not None:
                objects=objects.filter(pay_to_id=customer.account.id)
        if 'supplier_id' in kwargs:
            supplier=Customer.objects.filter(pk=kwargs['supplier']).first()
            if supplier is not None:
                objects=objects.filter(pay_to_id=supplier.account.id)
        return objects.all()
 


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
        self.customer= CustomerRepo(request=self.request).me
       

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

    def add_to_cart(self,*args, **kwargs):
        result=FAILED
        message=""
        cart_line=CartLine()

        if 'shop_id' in kwargs:
            cart_line.shop_id = kwargs['shop_id'] 

            
        if 'quantity' in kwargs:
            cart_line.quantity = kwargs['quantity'] 

        cart_line.customer = CustomerRepo(request=self.request).me
        cart_line.row = 1
        cart_line.save()
        if cart_line is not None:
            result=SUCCEED
            message="با موفقیت اضافه شد."
        CartLine.objects.filter(shop_id=cart_line.shop_id).filter(customer_id=cart_line.customer_id).exclude(id=cart_line.pk).delete()
        return (result,cart_line,message)

    def checkout(self,*args, **kwargs):
        message=""
        result=FAILED
        cart=None
        customer=CustomerRepo(request=self.request).customer(**kwargs)
        if not customer.account.profile.user==self.request.user:
            return result,message,cart
        for edited_cart_line in kwargs['cart_lines']:
            cart_line=CartLine()
            cart_line.customer=customer
            cart_line.shop_id=edited_cart_line['shop_id']
            cart_line.quantity=edited_cart_line['quantity']
            cart_line.save()
        cart_lines=customer.cartline_set.all()
        market_invoices=[]
        for cart_line in cart_lines:
            result=FAILED
            new_market_invoice=None
            pay_from_id=cart_line.shop.supplier.account.id
            pay_to_id=customer.account.id
            for market_invoice in market_invoices:
                if market_invoice.pay_from_id==pay_from_id:
                    new_market_invoice=market_invoice
            if new_market_invoice is None:
                new_market_invoice=MarketInvoice()
                new_market_invoice.pay_from_id=pay_from_id
                new_market_invoice.pay_to_id=pay_to_id
                new_market_invoice.title=f"سفارش جدید {customer.account.title} از {cart_line.shop.supplier.title}"
                new_market_invoice.invoice_datetime=timezone.now()
                new_market_invoice.save()
                market_invoices.append(new_market_invoice)
            leolog(new_market_invoice=new_market_invoice)
            market_invoice_line=InvoiceLine()
            market_invoice_line.invoice=new_market_invoice
            market_invoice_line.product_or_service=cart_line.shop.product_or_service
            market_invoice_line.quantity=cart_line.quantity
            market_invoice_line.unit_price=cart_line.shop.unit_price
            market_invoice_line.unit_name=cart_line.shop.unit_name
            market_invoice_line.save()
            result=SUCCEED

            message="""با موفقیت خرید شد."""
            for market_invoice in market_invoices:

                message+=f"""<a class="mx-2" href="{market_invoice.get_absolute_url()}">{market_invoice.title}</a>"""
            if result==SUCCEED:
                cart_line.delete()
        leolog(market_invoices=market_invoices,message=message,result=result)
        # market_invoice=MarketInvoice()
        # market_invoice.save()
        # market_invoices.append(market_invoice)
        return market_invoices,result,message
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
        if 'level' in kwargs:
            objects=objects.filter(level=kwargs['level'])
        return objects.all()

    def add_shop(self,*args, **kwargs):
        if not self.user.has_perm(APP_NAME+".add_shop"):
            return None
        shop=Shop()
        if 'product_or_service_id' in kwargs:
            shop.product_or_service_id = kwargs['product_or_service_id'] 
        if 'productorservice_id' in kwargs:
            shop.product_or_service_id = kwargs['productorservice_id'] 
        if 'product_id' in kwargs:
            shop.product_or_service_id = kwargs['product_id'] 
        if 'unit_name' in kwargs:
            shop.unit_name = kwargs['unit_name'] 
        if 'supplier_id' in kwargs:
            shop.supplier_id = kwargs['supplier_id'] 

        if 'old_price' in kwargs:
            shop.old_price = kwargs['old_price'] 
        if 'buy_price' in kwargs:
            shop.buy_price = kwargs['buy_price']
        if 'unit_price' in kwargs:
            shop.unit_price = kwargs['unit_price'] 

       
            
        if 'available' in kwargs:
            shop.available = kwargs['available'] 
        if 'level' in kwargs:
            shop.level = kwargs['level'] 
        if 'expire_datetime' in kwargs:
            shop.expire_datetime = kwargs['expire_datetime'] 

        shop.save()
        if 'specifications' in kwargs:
            specifications = kwargs['specifications']
            for specification in specifications:
                specification=ProductSpecification.objects.filter(pk=specification['id']).first()
                if specification is not None:
                    shop.specifications.add(specification)
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
    def in_cart(self,*args, **kwargs):
        
        objects = self.objects
        if 'product_or_service_id' in kwargs:
            objects=objects.filter(shop__product_or_service_id=kwargs['product_or_service_id'])
        if 'productorservice_id' in kwargs:
            objects=objects.filter(shop__product_or_service_id=kwargs['productorservice_id'])
        if 'unit_name' in kwargs:
            objects=objects.filter(shop__unit_name=kwargs['unit_name'])
        if 'shop_id' in kwargs:
            objects=objects.filter(shop_id=kwargs['shop_id'])
        if 'customer_id' in kwargs:
            objects=objects.filter(customer_id=kwargs['customer_id'])
        in_cart=0
        in_cart_unit=UnitNameEnum.ADAD
        for a in objects:
            in_cart+=a.quantity
            in_cart_unit=a.shop.unit_name
        return (in_cart,in_cart_unit)
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


        