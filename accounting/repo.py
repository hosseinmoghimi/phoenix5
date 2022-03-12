from .apps import APP_NAME
from .models import Account, FinancialDocument, FinancialYear, Invoice, Product,Service, SubAccount, Transaction
from django.db.models import Q
from authentication.repo import ProfileRepo
from django.utils import timezone
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
        if self.user.has_perm(APP_NAME+".view_financialdocument"):
            self.objects = FinancialDocument.objects.order_by('transaction__transaction_datetime')
        elif self.profile is not None:
            self.objects = FinancialDocument.objects.filter(account__profile=self.profile).order_by('document_datetime')
        else:
            self.objects = FinancialDocument.objects.filter(pk__lte=0).order_by('document_datetime')

    def list(self, *args, **kwargs):
        objects = self.objects.all()
        if 'category_id' in kwargs:
            objects = objects.filter(category_id=kwargs['category_id'])
        if 'for_home' in kwargs:
            objects = objects.filter(for_home=kwargs['for_home'])
        if 'search_for' in kwargs:
            search_for=kwargs['search_for']
            objects = objects.filter(title__contains=search_for) 
        if 'account_id' in kwargs:
            account_id=kwargs['account_id']
            objects = objects.filter(account_id=account_id) 
        return objects

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
        if 'document_datetime' in kwargs:
            financial_document_.document_datetime= kwargs['document_datetime']
        else:
            financial_document_.document_datetime= timezone.now()

        if 'financial_year_id' in kwargs:
            financial_document_.financial_year_id= kwargs['financial_year_id']
        else:
            financial_year= FinancialYearRepo(request=self.request).financial_year(date=financial_document_.document_datetime)
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
        self.user = None
        if 'request' in kwargs:
            self.request = kwargs['request']
            self.user = self.request.user
        if 'user' in kwargs:
            self.user = kwargs['user']
        
        self.objects=Account.objects.all()
        self.profile=ProfileRepo(*args, **kwargs).me
       

    def account(self, *args, **kwargs):
        pk=0
        if 'account_id' in kwargs:
            pk=kwargs['account_id']
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
       

    def invoice(self, *args, **kwargs):
        pk=0
        if 'invoice_id' in kwargs:
            pk=kwargs['invoice_id']
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

   

class TransactionRepo():
    def __init__(self, *args, **kwargs):
        self.request = None
        self.user = None
        if 'request' in kwargs:
            self.request = kwargs['request']
            self.user = self.request.user
        if 'user' in kwargs:
            self.user = kwargs['user']
        
        self.objects=Transaction.objects.all()
        self.profile=ProfileRepo(*args, **kwargs).me
       
        if self.user.has_perm(APP_NAME+".view_transaction"):
            self.objects = self.objects
        elif self.profile is not None:
            self.objects = self.objects.filter(Q(pay_from__profile=self.profile)|Q(pay_to__profile=self.profile))
        else:
            self.objects = self.objects.filter(pk=0)

    def transaction(self, *args, **kwargs):
        pk=0
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
        return objects.all()

   




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

   

