from datetime import timedelta
from urllib import request
from accounting.enums import FinancialDocumentTypeEnum, TransactionStatusEnum

from core.enums import UnitNameEnum
from utility.calendar import PersianCalendar
from .apps import APP_NAME
from .models import Account, Asset, Cheque, FinancialBalance, FinancialDocument, FinancialYear, Invoice, InvoiceLine, Payment, Price, Product,Service, Transaction
from django.db.models import Q
from authentication.repo import ProfileRepo
from django.utils import timezone


class AssetRepo():
    def __init__(self, *args, **kwargs):
        self.request = None
        self.user = None
        if 'request' in kwargs:
            self.request = kwargs['request']
            self.user = self.request.user
        if 'user' in kwargs:
            self.user = kwargs['user']
        
        self.objects=Asset.objects.all()
        self.profile=ProfileRepo(*args, **kwargs).me
       

    def asset(self, *args, **kwargs):
        pk=0
        if 'asset' in kwargs:
            return kwargs['asset']
        if 'asset_id' in kwargs:
            pk=kwargs['asset_id']
        elif 'pk' in kwargs:
            pk=kwargs['pk']
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

    def add_product(self,*args, **kwargs):
        if not self.user.has_perm(APP_NAME+".add_product"):
            return None
 
        if 'title' in kwargs:
            title = kwargs['title']

        product=Product()
        product.title=title
        product.save()
        return product



class ProductRepo():
    def __init__(self, *args, **kwargs):
        self.request = None
        self.user = None
        if 'request' in kwargs:
            self.request = kwargs['request']
            self.user = self.request.user
        if 'user' in kwargs:
            self.user = kwargs['user']
        
        self.objects=Product.objects.all()
        self.profile=ProfileRepo(*args, **kwargs).me
       

    def product(self, *args, **kwargs):
        pk=0
        if 'product' in kwargs:
            return kwargs['product']
        if 'product_id' in kwargs:
            pk=kwargs['product_id']
        elif 'pk' in kwargs:
            pk=kwargs['pk']
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

    def add_product(self,*args, **kwargs):
        if not self.user.has_perm(APP_NAME+".add_product"):
            return None
 
        if 'title' in kwargs:
            title = kwargs['title']

        product=Product()
        product.title=title
        product.save()
        return product


class ServiceRepo():
    def __init__(self, *args, **kwargs):
        self.request = None
        self.user = None
        if 'request' in kwargs:
            self.request = kwargs['request']
            self.user = self.request.user
        if 'user' in kwargs:
            self.user = kwargs['user']
        
        self.objects=Service.objects.all()
        self.profile=ProfileRepo(*args, **kwargs).me
       

    def service(self, *args, **kwargs):
        pk=0
        if 'service_id' in kwargs:
            pk=kwargs['service_id']
        elif 'pk' in kwargs:
            pk=kwargs['pk']
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

    def add_service(self,*args, **kwargs):
        if not self.user.has_perm(APP_NAME+".add_service"):
            return None
 
        if 'title' in kwargs:
            title = kwargs['title']

        service=Service()
        service.title=title
        service.save()
        return service


class FinancialBalanceRepo:
    def __init__(self, *args, **kwargs):
        self.request = None
        self.user = None
        if 'request' in kwargs:
            self.request = kwargs['request']
            self.user = self.request.user
        if 'user' in kwargs:
            self.user = kwargs['user']
        self.profile = ProfileRepo(user=self.user).me
        self.objects = FinancialBalance.objects.all()
        if self.user.has_perm(APP_NAME+".view_financialbalance"):
            self.objects = self.objects.all()
        elif self.profile is not None:
            self.objects = self.objects.filter(financial_document__account__profile=self.profile)
        else:
            self.objects = self.objects.filter(pk=0)


    def list(self, *args, **kwargs):
        objects = self.objects.all()
        if 'for_home' in kwargs:
            objects = objects.filter(for_home=kwargs['for_home'])
        if 'search_for' in kwargs:
            search_for=kwargs['search_for']
            objects = objects.filter(title__contains=search_for) 
        if 'account_id' in kwargs:
            account_id=kwargs['account_id']
            objects = objects.filter(financial_document__account_id=account_id) 
        if 'transaction_id' in kwargs:
            objects = objects.filter(financial_document__transaction_id=kwargs['transaction_id'])
        if 'financial_document_id' in kwargs:
            financial_document_id=kwargs['financial_document_id']
            objects = objects.filter(financial_document_id=financial_document_id) 
        return objects
    def add_financial_balance(self,*args, **kwargs):
        if not self.user.has_perm(APP_NAME+".add_financialbalance"):
            return None
        financial_balance=FinancialBalance()
        if 'title' in kwargs:
            financial_balance.title = kwargs['title']
        if 'bedehkar' in kwargs:
            financial_balance.bedehkar = kwargs['bedehkar']
        if 'bestankar' in kwargs:
            financial_balance.bestankar = kwargs['bestankar']
        if 'financial_document_id' in kwargs:
            financial_balance.financial_document_id = kwargs['financial_document_id']
        financial_balance.bestankar=0
        financial_balance.bedehkar=0
     
        financial_balance.save()
        if 'amount' in kwargs:

            if financial_balance.financial_document.direction==FinancialDocumentTypeEnum.BEDEHKAR:
                financial_balance.bedehkar=kwargs['amount']
            if financial_balance.financial_document.direction==FinancialDocumentTypeEnum.BESTANKAR:
                financial_balance.bestankar=kwargs['amount']
            financial_balance.save()
        # financial_balance.financial_document.normalize_balances()
        financial_balance.financial_document.normalize_sub_accounts()
        return financial_balance.financial_document.financialbalance_set.all()
    def financial_balance(self, *args, **kwargs):
            
        if 'financial_balance_id' in kwargs:
            return self.objects.filter(pk= kwargs['financial_balance_id']).first()
        if 'pk' in kwargs:
            return self.objects.filter(pk= kwargs['pk']).first()
        if 'id' in kwargs:
            return self.objects.filter(pk= kwargs['id']).first()


class PriceRepo:
    def __init__(self, *args, **kwargs):
        self.request = None
        self.user = None
        if 'request' in kwargs:
            self.request = kwargs['request']
            self.user = self.request.user
        if 'user' in kwargs:
            self.user = kwargs['user']
        self.profile = ProfileRepo(user=self.user).me
        self.objects = Price.objects.order_by('-date_added')
        if self.user.has_perm(APP_NAME+".view_price"):
            self.objects = self.objects.all()
        elif self.profile is not None:
            self.objects = self.objects.filter(account__profile_id=self.profile.id)
        else:
            self.objects = self.objects.filter(pk=0)


    def list(self, *args, **kwargs):
        objects = self.objects.all()
        if 'for_home' in kwargs:
            objects = objects.filter(for_home=kwargs['for_home'])
        if 'search_for' in kwargs:
            search_for=kwargs['search_for']
            objects = objects.filter(title__contains=search_for) 
        if 'account_id' in kwargs:
            account_id=kwargs['account_id']
            objects = objects.filter(account_id=account_id) 
        if 'item_id' in kwargs:
            item_id=kwargs['item_id']
            objects = objects.filter(product_or_service_id=item_id) 
        if 'product_or_service_id' in kwargs:
            product_or_service_id=kwargs['product_or_service_id']
            objects = objects.filter(product_or_service_id=product_or_service_id)  
        if 'product_id' in kwargs:
            item_id=kwargs['product_id']
            objects = objects.filter(product_or_service_id=item_id)  
        if 'service_id' in kwargs:
            item_id=kwargs['service_id']
            objects = objects.filter(product_or_service_id=item_id) 
        return objects
    def add_price(self,*args, **kwargs):
        
        account_id=0
        if self.request.user.has_perm(APP_NAME+".add_price") and 'account_id' in kwargs:
            account_id=kwargs['account_id']
        else:
            account=AccountRepo(request=self.request).me
            if account is not None :
                account_id=account.id

        if account_id ==0 or account_id is None:
            return
        unit_name=UnitNameEnum.ADAD
        product_or_service_id=0
        if 'product_or_service_id' in kwargs:
            product_or_service_id=kwargs['product_or_service_id']
        if 'unit_name' in kwargs:
            unit_name=kwargs['unit_name']
        sell_price=0
        if 'sell_price' in kwargs:
            sell_price=kwargs['sell_price']
        buy_price=0
        if 'buy_price' in kwargs:
            buy_price=kwargs['buy_price']
        price=Price()
        price.product_or_service_id=product_or_service_id
        price.buy_price=buy_price
        price.sell_price=sell_price
        price.account_id=account_id
        price.unit_name=unit_name
        if price.sell_price<=0 and account_id>0:
            return
        try:
            price.save()
            return price
        except:
            return

    def price(self, *args, **kwargs):
        if 'price_id' in kwargs:
            return self.objects.filter(pk= kwargs['price_id']).first()
        if 'pk' in kwargs:
            return self.objects.filter(pk= kwargs['pk']).first()
        if 'id' in kwargs:
            return self.objects.filter(pk= kwargs['id']).first()
   
   
class FinancialYearRepo:
    def __init__(self, *args, **kwargs):
        self.request = None
        self.user = None
        if 'request' in kwargs:
            self.request = kwargs['request']
            self.user = self.request.user
        if 'user' in kwargs:
            self.user = kwargs['user']
        self.objects = FinancialYear.objects.all()
        self.profile = ProfileRepo(user=self.user).me

    def list(self, *args, **kwargs):
        objects = self.objects.all()
        if 'for_home' in kwargs:
            objects = objects.filter(for_home=kwargs['for_home'])
        if 'search_for' in kwargs:
            search_for=kwargs['search_for']
            objects = objects.filter(title__contains=search_for) 
        if 'account_id' in kwargs:
            account_id=kwargs['account_id']
            objects = objects.filter(account_id=account_id) 
        return objects

    def financial_year(self, *args, **kwargs):
        if 'date' in kwargs:
            return self.objects.filter(start_date__lte=kwargs['date']).filter(end_date__gte=kwargs['date']).first()
           
        if 'financial_year_id' in kwargs:
            return self.objects.filter(pk= kwargs['financial_year_id']).first()
        if 'pk' in kwargs:
            return self.objects.filter(pk= kwargs['pk']).first()
        if 'id' in kwargs:
            return self.objects.filter(pk= kwargs['id']).first()
   

class FinancialDocumentRepo:
    def __init__(self, *args, **kwargs):
        self.request = None
        self.user = None
        if 'request' in kwargs:
            self.request = kwargs['request']
            self.user = self.request.user
        if 'user' in kwargs:
            self.user = kwargs['user']
        self.profile = ProfileRepo(user=self.user).me
        self.objects=FinancialDocument.objects
        if self.user.has_perm(APP_NAME+".view_financialdocument"):
            self.objects = self.objects
        elif self.profile is not None:
            self.objects = self.objects.filter(account__profile=self.profile)
        else:
            self.objects = self.objects.filter(pk__lte=0)

    def list(self, *args, **kwargs):
        objects = self.objects.all()
        if 'category_id' in kwargs:
            objects = objects.filter(category_id=kwargs['category_id'])
        if 'for_home' in kwargs:
            objects = objects.filter(for_home=kwargs['for_home'])
        if 'start_date' in kwargs and kwargs['start_date'] is not None:
            objects = objects.filter(transaction__transaction_datetime__gte=kwargs['start_date'])
        if 'end_date' in kwargs and kwargs['end_date'] is not None:
            objects = objects.filter(transaction__transaction_datetime__lte=kwargs['end_date'])
        if 'profile_id' in kwargs and kwargs['profile_id'] is not None is not None and kwargs['profile_id']>0:
            objects = objects.filter(account__profile_id=kwargs['profile_id'])
        if 'search_for' in kwargs and kwargs['search_for'] is not None:
            search_for=kwargs['search_for']
            objects = objects.filter(Q(transaction__title__contains=search_for)|Q(transaction__short_description__contains=search_for)|Q(transaction__description__contains=search_for))
        if 'transaction_id' in kwargs and kwargs['transaction_id'] is not None is not None and kwargs['transaction_id']>0:
            objects = objects.filter(transaction_id=kwargs['transaction_id'])
        if 'account_id' in kwargs and kwargs['account_id'] is not None and kwargs['account_id']>0:
            account_id=kwargs['account_id']
            objects = objects.filter(account_id=account_id) 
        return objects.order_by('transaction__transaction_datetime')

    def financial_document(self, *args, **kwargs):
        if 'financial_document_id' in kwargs:
            return self.objects.filter(pk= kwargs['financial_document_id']).first()
        if 'pk' in kwargs:
            return self.objects.filter(pk= kwargs['pk']).first()
        if 'id' in kwargs:
            return self.objects.filter(pk= kwargs['id']).first()
            
    def add_financial_document(self, *args, **kwargs):
        if not self.user.has_perm(APP_NAME+".add_financialdocument"):
            return
        financial_document_=FinancialDocument()
        

        if 'financial_year_id' in kwargs:
            financial_document_.financial_year_id= kwargs['financial_year_id']
        else:
            financial_year= FinancialYearRepo(request=self.request).financial_year(date=financial_document_.transaction.transaction_datetime)
            financial_document_.financial_year_id= financial_year.id

        if 'account_id' in kwargs:
            financial_document_.account_id= kwargs['account_id']
        if 'title' in kwargs:
            financial_document_.title= kwargs['title']
        if 'bestankar' in kwargs:
            financial_document_.bestankar= kwargs['bestankar']
        if 'bedehkar' in kwargs:
            financial_document_.bedehkar= kwargs['bedehkar']
        if 'category_id' in kwargs:
            financial_document_.category_id= kwargs['category_id']
        financial_document_.save()
        return financial_document_


class AccountRepo():
    def __init__(self, *args, **kwargs):
        self.request = None
        self.me=None
        self.user = None
        if 'request' in kwargs:
            self.request = kwargs['request']
            self.user = self.request.user
        if 'user' in kwargs:
            self.user = kwargs['user']
        
        self.objects=Account.objects.all()
        self.profile=ProfileRepo(*args, **kwargs).me
        if self.profile is not None:
            self.me=Account.objects.filter(profile=self.profile).first()
        

    def account(self, *args, **kwargs):
        pk=0
        if 'account_id' in kwargs:
            account_id=kwargs['account_id']
            return self.objects.filter(pk=account_id).first()
        if 'profile_id' in kwargs:
            profile_id=kwargs['profile_id']
            profile= ProfileRepo(request=self.request).profile(profile_id=profile_id)
            account=Account.objects.filter(profile_id=profile_id).first()
            if account is None:
                account=Account()
                account.profile_id=profile.id
                account.save()
                return account
        elif 'pk' in kwargs:
            pk=kwargs['pk']
            return self.objects.filter(pk=pk).first()
        elif 'id' in kwargs:
            id=kwargs['id']
            return self.objects.filter(pk=id).first()
     
    def list(self, *args, **kwargs):
        objects = self.objects
        if 'search_for' in kwargs:
            search_for=kwargs['search_for']
            objects = objects.filter(Q(title__contains=search_for))
        if 'for_home' in kwargs:
            objects = objects.filter(Q(for_home=kwargs['for_home']))
        if 'search_for' in kwargs:
            objects=objects.filter(title__contains=kwargs['search_for'])
        if 'profile_id' in kwargs:
            objects=objects.filter(profile_id=kwargs['profile_id'])
        if 'parent_id' in kwargs:
            objects=objects.filter(parent_id=kwargs['parent_id'])
        return objects.all()
    def my_list(self,*args, **kwargs):
        if self.request.user.has_perm(APP_NAME+".view_account"):
            return self.objects.all()
        else:
            return self.objects.filter(profile=self.profile)
   

class InvoiceLineRepo():
    def __init__(self, *args, **kwargs):
        self.request = None
        self.me=None
        self.user = None
        if 'request' in kwargs:
            self.request = kwargs['request']
            self.user = self.request.user
        if 'user' in kwargs:
            self.user = kwargs['user']
        
        self.objects=InvoiceLine.objects.all()
        self.profile=ProfileRepo(*args, **kwargs).me
        if self.profile is not None:
            self.me=Account.objects.filter(profile=self.profile).first()
        

    def invoice_line(self, *args, **kwargs):
        pk=0
        if 'invoice_line_id' in kwargs:
            account_id=kwargs['invoice_line_id']
            return self.objects.filter(pk=account_id).first()
        
        elif 'pk' in kwargs:
            pk=kwargs['pk']
            return self.objects.filter(pk=pk).first()
        elif 'id' in kwargs:
            id=kwargs['id']
            return self.objects.filter(pk=id).first()
     
    def list(self, *args, **kwargs):
        objects = self.objects
        if 'search_for' in kwargs:
            search_for=kwargs['search_for']
            objects = objects.filter(Q(title__contains=search_for))
        if 'for_home' in kwargs:
            objects = objects.filter(Q(for_home=kwargs['for_home']))
        if 'search_for' in kwargs:
            objects=objects.filter(title__contains=kwargs['search_for'])
        if 'profile_id' in kwargs:
            objects=objects.filter(profile_id=kwargs['profile_id'])
        if 'parent_id' in kwargs:
            objects=objects.filter(parent_id=kwargs['parent_id'])
        return objects.all()
    def my_list(self,*args, **kwargs):
        if self.request.user.has_perm(APP_NAME+".view_account"):
            return self.objects.all()
        else:
            return self.objects.filter(profile=self.profile)
   

class PaymentRepo():
    def __init__(self, *args, **kwargs):
        self.request = None
        self.me=None
        self.user = None
        if 'request' in kwargs:
            self.request = kwargs['request']
            self.user = self.request.user
        if 'user' in kwargs:
            self.user = kwargs['user']
        
        self.objects=Payment.objects
        self.profile=ProfileRepo(*args, **kwargs).me
        if self.user.has_perm(APP_NAME+".view_payment"):
            self.objects=self.objects
        elif self.profile is not None:
            self.objects=self.objects.filter(Q(pay_from__profile_id=self.profile.id)|Q(pay_to__profile_id=self.profile.id))
        

    def payment(self, *args, **kwargs):
        pk=0
        if 'payment_id' in kwargs:
            pk=kwargs['payment_id']
        elif 'pk' in kwargs:
            pk=kwargs['pk']
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
        if 'account_id' in kwargs:
            objects=objects.filter(Q(pay_to_id=kwargs['account_id'])|Q(pay_from_id=kwargs['account_id']))
        if 'profile_id' in kwargs:
            objects=objects.filter(account__profile_id=kwargs['profile_id'])
        return objects.order_by('transaction_datetime')

    def add_payment(self,*args, **kwargs):
        if not self.request.user.has_perm(APP_NAME+".add_payment"):
            return
        payment=Payment()
        payment.creator=self.profile
        if 'title' in kwargs:
            payment.title=kwargs['title']

        if 'pay_from_id' in kwargs:
            payment.pay_from_id=kwargs['pay_from_id']
        if 'description' in kwargs:
            payment.description=kwargs['description']
        if 'pay_to_id' in kwargs:
            payment.pay_to_id=kwargs['pay_to_id']
        if 'amount' in kwargs:
            payment.amount=kwargs['amount']
        if 'payment_method' in kwargs:
            payment.payment_method=kwargs['payment_method']

        if 'payment_datetime' in kwargs:
            payment.transaction_datetime=kwargs['payment_datetime']

        if 'transaction_datetime' in kwargs:
            payment.transaction_datetime=kwargs['transaction_datetime']

        
        # if 'financial_year_id' in kwargs:
        #     payment.financial_year_id=kwargs['financial_year_id']
        # else:
        #     payment.financial_year_id=FinancialYear.get_by_date(date=payment.transaction_datetime).id

        payment.save()
        return payment


class InvoiceRepo():
    def __init__(self, *args, **kwargs):
        self.request = None
        self.user = None
        if 'request' in kwargs:
            self.request = kwargs['request']
            self.user = self.request.user
        if 'user' in kwargs:
            self.user = kwargs['user']
        
        self.objects=Invoice.objects.all()
        self.profile=ProfileRepo(*args, **kwargs).me

    def create_invoice(self,*args, **kwargs):
        if not self.user.has_perm(APP_NAME+".add_invoice"):

            return
        me_account=AccountRepo(request=self.request).me
        if me_account is None:
            return
        pay_from_id=me_account.id
        if 'pay_from_id' in kwargs and kwargs['pay_from_id'] is not None and kwargs['pay_from_id']>0:
            pay_from_id=kwargs['pay_from_id']
        pay_to_id=me_account.id
        if 'pay_to_id' in kwargs and kwargs['pay_to_id'] is not None and kwargs['pay_to_id']>0:
            pay_to_id=kwargs['pay_to_id']
        now=PersianCalendar().date
        invoice=Invoice()
        invoice.pay_from_id=pay_from_id
        invoice.pay_to_id=pay_to_id
        invoice.invoice_datetime=now
        invoice.save()
        invoice.title=f"فاکتور شماره {invoice.pk}"
        invoice.save()
        return invoice

    def invoice(self, *args, **kwargs):
        if 'invoice' in kwargs:
            return kwargs['invoice']
        if 'invoice_id' in kwargs:
            return self.objects.filter(pk=kwargs['invoice_id']).first()
        elif 'pk' in kwargs:
            return self.objects.filter(pk=kwargs['pk']).first()
        elif 'id' in kwargs:
            return self.objects.filter(pk=kwargs['id']).first()
     
    def list(self, *args, **kwargs):
        objects = self.objects
        if 'search_for' in kwargs:
            search_for=kwargs['search_for']
            objects = objects.filter(Q(title__contains=search_for)|Q(short_description__contains=search_for)|Q(description__contains=search_for))
        if 'for_home' in kwargs:
            objects = objects.filter(Q(for_home=kwargs['for_home']))
        if 'product_id' in kwargs:
            product_id=kwargs['product_id']
            invoice_lines=InvoiceLine.objects.filter(product_or_service_id=product_id)
            ids=(invoice_line.invoice_id for invoice_line in invoice_lines)
            objects= objects.filter(id__in=ids)
        return objects.all()

   
    def edit_invoice(self,*args, **kwargs):
        
        invoice=self.invoice(*args, **kwargs)
        if invoice is None:
            return
        if self.user.has_perm(APP_NAME+".change_invoice"):
            pass
        elif invoice.pay_from.profile==self.profile:
            pass
        else:
            return
        if invoice.status==TransactionStatusEnum.DELIVERED:
            return None
        if invoice.status==TransactionStatusEnum.APPROVED:
            return None
        if 'title' in kwargs:
            invoice.title=kwargs['title']
        if 'pay_from_id' in kwargs:
            invoice.pay_from_id=kwargs['pay_from_id']

        if 'payment_method' in kwargs:
            invoice.payment_method=kwargs['payment_method']

        if 'status' in kwargs:
            invoice.status=kwargs['status']

        if 'pay_to_id' in kwargs:
            invoice.pay_to_id=kwargs['pay_to_id']

        if 'invoice_datetime' in kwargs:
            invoice.invoice_datetime=kwargs['invoice_datetime']
            invoice.transaction_datetime=kwargs['invoice_datetime']

        if 'description' in kwargs:
            invoice.description=kwargs['description']

        if 'discount' in kwargs:
            invoice.discount=kwargs['discount']

        if 'ship_fee' in kwargs:
            invoice.ship_fee=kwargs['ship_fee']

        if 'tax_percent' in kwargs:
            invoice.tax_percent=kwargs['tax_percent']

        invoice.save()
        if 'lines' in kwargs:
            lines=kwargs['lines']
            for line in lines:
                if int(line['quantity'])>0:
                    sw=False
                    for line_origin in invoice.lines.all():
                        b=line_origin.product_or_service_id
                        a=line['product_or_service_id']
                        if line_origin.product_or_service_id==line['product_or_service_id']:
                            line_origin.quantity=int(line['quantity'])
                            line_origin.unit_price=int(line['unit_price'])
                            line_origin.unit_name=line['unit_name']
                            line_origin.save()
                            sw=True
                    if not sw:
                        invoice_line=InvoiceLine()
                        invoice_line.invoice=invoice
                        invoice_line.product_or_service_id=int(line['product_or_service_id'])
                        invoice_line.quantity=int(line['quantity'])
                        invoice_line.row=int(line['row'])
                        invoice_line.unit_price=int(line['unit_price'])
                        invoice_line.unit_name=line['unit_name']
                        invoice_line.save()
        
        invoice.save()
        return invoice


class ChequeRepo():
    def __init__(self, *args, **kwargs):
        self.request = None
        self.user = None
        if 'request' in kwargs:
            self.request = kwargs['request']
            self.user = self.request.user
        if 'user' in kwargs:
            self.user = kwargs['user']
        
        self.objects=Cheque.objects.all()
        self.profile=ProfileRepo(*args, **kwargs).me
       
    def add_cheque(self,*args, **kwargs):
        if not self.request.user.has_perm(APP_NAME+".add_cheque"):
            return
        cheque=Cheque()
        me_acc=AccountRepo(request=self.request).me

        if 'title' in kwargs:
            cheque.title=kwargs['title']
        if 'cheque_date' in kwargs:
            cheque.cheque_date=kwargs['cheque_date']
        else:
            cheque.cheque_date=PersianCalendar().date


            
        if 'pay_to_id' in kwargs:
            cheque.pay_to_id=kwargs['pay_to_id']
        else:
            cheque.pay_to_id=me_acc.id
        if 'pay_from_id' in kwargs:
            cheque.pay_from_id=kwargs['pay_from_id']
        else:
            cheque.pay_from_id=me_acc.id


        cheque.creator=self.profile


        if 'transaction_datetime' in kwargs:
            cheque.transaction_datetime=kwargs['transaction_datetime']
        else:
            cheque.transaction_datetime=PersianCalendar().date
            
        if 'amount' in kwargs:
            cheque.amount=kwargs['amount']
        else:
            cheque.amount=0


        cheque.save()
        return cheque

    def cheque(self, *args, **kwargs):
        pk=0
        if 'cheque_id' in kwargs:
            pk=kwargs['cheque_id']
            return self.objects.filter(pk=pk).first()
        if 'pk' in kwargs:
            pk=kwargs['pk']
            return self.objects.filter(pk=pk).first()
        if 'id' in kwargs:
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


class TransactionRepo():
    def __init__(self, *args, **kwargs):
        self.request = None
        self.user = None
        if 'request' in kwargs:
            self.request = kwargs['request']
            self.user = self.request.user
        if 'user' in kwargs:
            self.user = kwargs['user']
        
        self.objects=Transaction.objects
        self.profile=ProfileRepo(*args, **kwargs).me
       
        if self.user.has_perm(APP_NAME+".view_transaction"):
            self.objects = self.objects
        elif self.profile is not None:
            self.objects = self.objects.filter(Q(pay_from__profile=self.profile)|Q(pay_to__profile=self.profile))
        else:
            self.objects = self.objects.filter(pk=0)

    def transaction(self, *args, **kwargs):
        pk=0
        if 'transaction' in kwargs:
            return kwargs['transaction']
        if 'transaction_id' in kwargs:
            pk=kwargs['transaction_id']
        elif 'pk' in kwargs:
            pk=kwargs['pk']
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
        if 'account_id' in kwargs:
            objects=objects.filter(Q(pay_from_id=kwargs['account_id'])|Q(pay_to_id=kwargs['account_id']))
        if 'account_id_1' in kwargs and 'account_id_2' in kwargs:
            account_id_1=kwargs['account_id_1']
            account_id_2=kwargs['account_id_2']
            objects = self.objects.filter(Q(pay_from_id=account_id_1)|Q(pay_from_id=account_id_2)).filter(Q(pay_to_id=account_id_1)|Q(pay_to_id=account_id_2))
        return objects.order_by('transaction_datetime')


class SubAccountRepo():
    def __init__(self, *args, **kwargs):
        self.request = None
        self.user = None
        if 'request' in kwargs:
            self.request = kwargs['request']
            self.user = self.request.user
        if 'user' in kwargs:
            self.user = kwargs['user']
        
        self.objects=SubAccount.objects.all()
        self.profile=ProfileRepo(*args, **kwargs).me
       

    def sub_account(self, *args, **kwargs):
        pk=0
        if 'sub_account_id' in kwargs:
            pk=kwargs['sub_account_id']
        elif 'pk' in kwargs:
            pk=kwargs['pk']
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

   




