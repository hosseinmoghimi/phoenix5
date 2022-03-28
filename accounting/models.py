from authentication.models import IMAGE_FOLDER
from phoenix.server_settings import STATIC_URL
from phoenix.settings import MEDIA_URL
from utility.currency import to_price
from utility.calendar import PERSIAN_MONTH_NAMES, PersianCalendar,to_persian_datetime_tag
from core.middleware import get_request
from django.db import models
from core.models import Page
from django.shortcuts import reverse
from django.utils.translation import gettext as _
from .apps import APP_NAME
from utility.utils import LinkHelper
from .enums import *
from tinymce.models import HTMLField
from core.enums import ColorEnum,UnitNameEnum
from django.utils import timezone
 
class Asset(Page,LinkHelper):
    
    class Meta:
        verbose_name = _("Asset")
        verbose_name_plural = _("Assets")
 


    def save(self,*args, **kwargs):
        if self.class_name is None or self.class_name=="":
            self.class_name='asset'
        if self.app_name is None or self.app_name=="":
            self.app_name=APP_NAME
        return super(Asset,self).save(*args, **kwargs)


class Price(models.Model,LinkHelper):
    account=models.ForeignKey("account", verbose_name=_("account"), on_delete=models.CASCADE)
    product_or_service=models.ForeignKey("productorservice", verbose_name=_("product_or_service"), on_delete=models.CASCADE)
    unit_name=models.CharField(_("unit_name"),choices=UnitNameEnum.choices,default=UnitNameEnum.ADAD, max_length=50)
    sell_price=models.IntegerField(_("فروش"),default=0)
    buy_price=models.IntegerField(_("خرید"),default=0)
    date_added=models.DateTimeField(_("date_added"), auto_now=False, auto_now_add=True)
    app_name=APP_NAME
    class_name="price"
    def persian_date_added(self,no_tag=False):
        if no_tag:
            return PersianCalendar().from_gregorian(self.date_added)
        return to_persian_datetime_tag(self.date_added)
    def profit_percentage(self):
        if self.buy_price<=0:
            return 100
        return int(100.0*(self.sell_price-self.buy_price)/self.buy_price)
    class Meta:
        verbose_name = _("Price")
        verbose_name_plural = _("Prices")

    def __str__(self):
        return f"""{self.product_or_service.title} @ {self.account} {self.persian_date_added(no_tag=True)}"""


class Transaction(Page,LinkHelper):
    pay_from=models.ForeignKey("account",related_name="transactions_from", verbose_name=_("پرداخت کننده"), on_delete=models.CASCADE)
    pay_to=models.ForeignKey("account", related_name="transactions_to",verbose_name=_("دریافت کننده"), on_delete=models.CASCADE)
    creator=models.ForeignKey("authentication.profile",null=True,blank=True, verbose_name=_("ثبت شده توسط"), on_delete=models.SET_NULL)
    status=models.CharField(_("وضعیت"),choices=TransactionStatusEnum.choices,default=TransactionStatusEnum.DRAFT, max_length=50)
    category=models.ForeignKey("transactioncategory",null=True,blank=True, verbose_name=_("دسته بندی"), on_delete=models.SET_NULL)
    amount=models.IntegerField(_("مبلغ"),default=0)
    payment_method=models.CharField(_("نوع پرداخت"),choices=PaymentMethodEnum.choices,default=PaymentMethodEnum.DRAFT, max_length=50)
    transaction_datetime=models.DateTimeField(_("تاریخ تراکنش"), auto_now=False, auto_now_add=False)
    def color(self):
        color="primary"
        if self.status==TransactionStatusEnum.DRAFT:
            color="secondary"
        if self.status==TransactionStatusEnum.APPROVED:
            color="success"
        if self.status==TransactionStatusEnum.IN_PROGRESS:
            color="warning"
        if self.status==TransactionStatusEnum.CANCELED:
            color="secondary"
        return color
    class Meta:
        verbose_name = _("Transaction")
        verbose_name_plural = _("Transactions")

    def __str__(self):
        return self.title 


    def save(self,*args, **kwargs):
        if self.transaction_datetime is None:
            from django.utils import timezone
            self.transaction_datetime=timezone.now()
        print(self.pay_from_id)
        super(Transaction,self).save(*args, **kwargs)
        # FinancialDocument.objects.filter(transaction=self).delete()

        fd_bedehkar=FinancialDocument.objects.filter(transaction=self).filter(account_id=self.pay_to.id).first()
        if fd_bedehkar is None:
            fd_bedehkar=FinancialDocument(transaction=self,account_id=self.pay_to.id,direction=FinancialDocumentTypeEnum.BEDEHKAR)
        fd_bedehkar.bestankar=0
        fd_bedehkar.bedehkar=self.amount
        fd_bedehkar.save()

        fd_bestankar=FinancialDocument.objects.filter(transaction=self).filter(account_id=self.pay_from.id).first()
        if fd_bestankar is None:
            fd_bestankar=FinancialDocument(transaction=self,account_id=self.pay_from.id,direction=FinancialDocumentTypeEnum.BESTANKAR)
        fd_bestankar.bestankar=self.amount
        fd_bestankar.bedehkar=0
        fd_bestankar.save()

    @property
    def persian_transaction_datetime(self,no_tag=False):
        if no_tag:
            return PersianCalendar().from_gregorian(self.transaction_datetime)
        return to_persian_datetime_tag(self.transaction_datetime)


class ProductOrService(Page):

    
    @property
    def unit_price(self):
        request=get_request()
        if request is not None:
             
            account=Account.objects.filter(profile__user_id=request.user.id).first()
            if account is not None:
                last_price=Price.objects.filter(sell_price__gt=0).filter(product_or_service=self).filter(account=account).order_by("-date_added").first()

                if last_price is not None:
                    return last_price.sell_price
        return 0

    @property
    def buy_price(self):
        request=get_request()
        if request is not None:
             
            account=Account.objects.filter(profile__user_id=request.user.id).first()
            last_price=Price.objects.filter(buy_price__gt=0).filter(product_or_service=self).filter(account=account).order_by("-date_added").first()

            if last_price is not None:
                return last_price.buy_price
        return 0
    @property
    def unit_name(self):
        return "عدد"

    class Meta:
        verbose_name = _("ProductOrService")
        verbose_name_plural = _("ProductOrServices")


class Product(ProductOrService):

    class Meta:
        verbose_name = _("Product")
        verbose_name_plural = _("Products")






    @property
    def available(self):
        id=0         
        return id
        
    def save(self,*args, **kwargs):
        if self.class_name is None or self.class_name=="":
            self.class_name='product'
        if self.app_name is None or self.app_name=="":
            self.app_name=APP_NAME
        return super(Product,self).save(*args, **kwargs)

 
class Service(ProductOrService):

    class Meta:
        verbose_name = _("Service")
        verbose_name_plural = _("Services")
 
 

    def save(self,*args, **kwargs):
        if self.class_name is None or self.class_name=="":
            self.class_name='service'
        if self.app_name is None or self.app_name=="":
            self.app_name=APP_NAME
        return super(Service,self).save(*args, **kwargs)


class Account(models.Model,LinkHelper):
    logo_origin=models.ImageField(_("logo"), null=True,blank=True,upload_to=IMAGE_FOLDER+"account/", height_field=None, width_field=None, max_length=None)
    title=models.CharField(_("title"), null=True,blank=True,max_length=500)
    profile=models.ForeignKey("authentication.profile", verbose_name=_("profile"), on_delete=models.CASCADE)
    class_name="account"
    app_name=APP_NAME
    def balance_rest(self):
        return self.balance['rest']
    def invoices(self):
        return Invoice.objects.filter(models.Q(pay_from=self)|models.Q(pay_to=self))

    def logo(self):
        if self.logo_origin:
            return MEDIA_URL+str(self.logo_origin)
        return self.profile.image
        # return f"{STATIC_URL}{APP_NAME}/img/account.png"
    @property
    def employee(self):
        from projectmanager.models import Employee
        return Employee.objects.filter(id=self.pk).first()
    class Meta:
        verbose_name = _("Account")
        verbose_name_plural = _("Accounts")
    def total_stock(self):
        sum=0
        for share_holder in  self.shareholder_set.all():
            sum+=share_holder.stock
        return sum
    def __str__(self):
        return self.title

    def save(self,*args, **kwargs):
        # from projectmanager.models import Employee
        # a=Account.objects.filter(fff="")
        if self.title is None or self.title=="":
            if self.profile is not None:
                self.title=self.profile.name
            else:
                self.title=self.profile_ptr_id
        super(Account,self).save(*args, **kwargs)
    
    @property
    def balance(self):
        balance={}
        bestankar=0
        bedehkar=0
        for doc in self.financialdocument_set.all():
            bestankar+=doc.bestankar
            bedehkar+=doc.bedehkar
        rest=bestankar-bedehkar
        balance['rest']=rest
        balance['bestankar']=bestankar
        balance['bedehkar']=bedehkar
        return balance


class Bank(models.Model):
    name=models.CharField(_("بانک"), max_length=50)
    branch=models.CharField(_("شعبه"),null=True,blank=True, max_length=50)
    address=models.CharField(_("آدرس"),null=True,blank=True, max_length=50)
    tel=models.CharField(_("تلفن"),null=True,blank=True, max_length=50)
    
    
    def __str__(self):
        return f"""بانک {self.name}  {(("شعبه "+self.branch) or "")}"""


    class Meta:
        verbose_name = _("Bank")
        verbose_name_plural = _("Banks")


class BankAccount(Account):
    bank=models.ForeignKey("bank", verbose_name=_("bank"), on_delete=models.CASCADE)
    account_no=models.CharField(_("shomareh"),null=True,blank=True, max_length=50)
    card_no=models.CharField(_("card"),null=True,blank=True, max_length=50)
    shaba_no=models.CharField(_("shaba"),null=True,blank=True, max_length=50)
    class_name='bankaccount'
    class Meta:
        verbose_name = _("BankAccount")
        verbose_name_plural = _("BankAccounts")

    def balance(self):
        return 0-self.rest()

    def get_absolute_url(self):
        return reverse(APP_NAME+":bank_account", kwargs={"pk": self.pk})


    def __str__(self):
        return self.title


    def save(self,*args, **kwargs):
        self.title=f"""حساب {self.bank} {self.profile.name}"""
        return super(BankAccount,self).save(*args, **kwargs)


class FinancialYear(models.Model):
    title=models.CharField(_("عنوان"), max_length=50)
    year=models.IntegerField(_("year"))
    start_date=models.DateTimeField(_("start_date"), auto_now=False, auto_now_add=False)
    end_date=models.DateTimeField(_("end_date"), auto_now=False, auto_now_add=False)
    def get_by_date(date):
        return FinancialYear.objects.filter(start_date__lte=date).filter(end_date__gte=date).first()
    
    def __str__(self):
        return self.title


    class Meta:
        verbose_name = _("FinancialYear")
        verbose_name_plural = _("FinancialYears")


class FinancialDocument(models.Model,LinkHelper):
    account=models.ForeignKey("account", verbose_name=_("account"), on_delete=models.CASCADE)
    bedehkar=models.IntegerField(_("bedehkar"),default=0)
    bestankar=models.IntegerField(_("bestankar"),default=0)
    document_datetime=models.DateTimeField(_("document_datetime"), auto_now=False, auto_now_add=True)
    transaction=models.ForeignKey("transaction",verbose_name=_("transaction"), on_delete=models.CASCADE)
    tags=models.ManyToManyField("FinancialDocumentTag", blank=True,verbose_name=_("tags"))
    color=models.CharField(_("color"),max_length=50,choices=ColorEnum.choices,default=ColorEnum.PRIMARY)
    direction=models.CharField(_("direction"),max_length=50,choices=FinancialDocumentTypeEnum.choices,default=FinancialDocumentTypeEnum.BESTANKAR)
    app_name=APP_NAME
    class_name="financialdocument"

    @property
    def rest(self):
        rest=0
        for fd in FinancialDocument.objects.filter(account=self.account).filter(document_datetime__lte=self.transaction.transaction_datetime):
            rest+=fd.bestankar
            rest-=fd.bedehkar
        return rest

    def get_state_badge(self):
        color="muted"
        state="خنثی"
        if self.bedehkar>0:
            color="danger"
            state="بدهکار"
        if self.bestankar>0:
            color="success"
            state="بستانکار"

        return f"""<span class="badge badge-{color}">{state}</span>"""


    @property
    def persian_document_datetime(self,no_tag=False):
        if no_tag:
            return PersianCalendar().from_gregorian(self.document_datetime)
        return to_persian_datetime_tag(self.document_datetime)
    @property
    def title(self):
        return self.transaction.title 
     
    
    

    class Meta:
        verbose_name = _("FinancialDocument")
        verbose_name_plural = _("FinancialDocuments")

    def __str__(self):
        return f"""{self.account.title} : {self.transaction.title} : {self.transaction.amount}"""
    def normalize_balances(self,*args, **kwargs):
        balances=FinancialBalance.objects.filter(financial_document=self)
        sum_bestankar=0
        sum_bedehkar=0
        for balance in balances:
            sum_bestankar+=balance.bestankar
            sum_bedehkar+=balance.bedehkar
        if not sum_bestankar==self.bestankar or not sum_bedehkar==self.bedehkar:
            b=FinancialBalance.objects.filter(financial_document=self).filter(title=FinancialBalanceTitleEnum.MISC).first()
            if b is None:
                b=FinancialBalance()
                b.financial_document=self
                b.title==FinancialBalanceTitleEnum.MISC
            b.bestankar=self.bestankar-sum_bestankar
            b.bedehkar=self.bedehkar-sum_bedehkar
            if b.bedehkar==0 and b.bestankar==0:
                return 
            else:
                b.save()
    def save(self,*args, **kwargs):
        super(FinancialDocument,self).save(*args, **kwargs)
       
    def is_bestankar(self):
        return self.bestankar>0 
    def is_bedehkar(self):
        return self.bedehkar>0


class FinancialBalance(models.Model,LinkHelper):
    app_name=APP_NAME
    class_name="financialbalance"
    title=models.CharField(_("title"),choices=FinancialBalanceTitleEnum.choices,default=FinancialBalanceTitleEnum.MISC, max_length=50)
    financial_document=models.ForeignKey("FinancialDocument", verbose_name=_("FinancialDocument"), on_delete=models.CASCADE)
    bestankar=models.IntegerField(_("بستانکار"),default=0)
    bedehkar=models.IntegerField(_("بدهکار"),default=0)
     
    def amount(self):
        return self.bedehkar+self.bestankar


    class Meta:
        verbose_name = _("FinancialBalance")
        verbose_name_plural = _("FinancialBalances")

    def __str__(self):
        return f"""{str(self.financial_document)} {self.title} {to_price(self.amount())}"""

    def save(self,*args, **kwargs):
        super(FinancialBalance,self).save(*args, **kwargs)
        # self.financial_document.normalize_sub_accounts()

class FinancialDocumentTag(models.Model):
    title=models.CharField(_("title"), max_length=50)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'FinancialDocumentTag'
        verbose_name_plural = 'FinancialDocumentTags'


class Cheque(Transaction,LinkHelper):
    cheque_date=models.DateField(_("تاریخ چک"), auto_now=False, auto_now_add=False)
    
    def persian_cheque_date(self,no_tag=False):
        if no_tag:
            return PersianCalendar().from_gregorian(self.cheque_date)
        return to_persian_datetime_tag(self.cheque_date)
    class Meta:
        verbose_name = _("چک")
        verbose_name_plural = _("چک ها")

    def __str__(self):
        return self.title
    
    def color(self):
        color='primary'
        if self.status==ChequeStatusEnum.DRAFT:
            return 'secondary'
        if self.status==ChequeStatusEnum.RETURNED:
            return 'danger'
        if self.status==ChequeStatusEnum.PAID:
            return 'success'
        if self.status==ChequeStatusEnum.PASSED:
            return 'success'

        return color


    def save(self,*args, **kwargs):
        if self.class_name is None or self.class_name=="":
            self.class_name='cheque'
        if self.app_name is None or self.app_name=="":
            self.app_name=APP_NAME
        super(Cheque,self).save(*args, **kwargs)


class TransactionCategory(models.Model):
    class_name="transactioncategory"
    title=models.CharField(_("title"), max_length=50)
    color_origin=models.CharField(_("color"),choices=ColorEnum.choices,null=True,blank=True, max_length=50)
    @property
    def color(self):
        if self.color_origin:
            return self.color_origin
        if self.title=="هزینه":
            return "danger"
        return 'primary'
    class Meta:
        verbose_name = 'TransactionCategory'
        verbose_name_plural = 'TransactionCategories'
    def get_absolute_url(self):
        return reverse(APP_NAME+":transactioncategory",kwargs={'pk':self.pk})
        
    def __str__(self):
        return self.title


class Invoice(Transaction):
    tax_percent=models.IntegerField(_("درصد مالیات"),default=9)
    invoice_datetime=models.DateTimeField(_("تاریخ فاکتور"), auto_now=False, auto_now_add=False)
    ship_fee=models.IntegerField(_("هزینه حمل"),default=0)
    discount=models.IntegerField(_("تخفیف"),default=0)

    def get_print_url(self):
        return reverse(APP_NAME+":invoice_print",kwargs={'pk':self.pk})
    def editable(self):
        if self.status==TransactionStatusEnum.DRAFT:
            return True
        if self.status==TransactionStatusEnum.IN_PROGRESS:
            return True
        return False
    def get_title(self):
        return self.title or f"فاکتور شماره {self.pk}"
  
    def get_edit_url2(self):
        return reverse(APP_NAME+":edit_invoice",kwargs={'pk':self.pk})
    def get_print_url(self):
        return reverse(APP_NAME+":invoice_print",kwargs={'pk':self.pk})
    
    
    def persian_invoice_datetime_tag(self):
        return to_persian_datetime_tag(self.invoice_datetime)
    def persian_invoice_datetime(self,no_tag=False):
        return PersianCalendar().from_gregorian(self.invoice_datetime)
    def tax_amount(self):
        
        sum=self.lines_total()
        sum+=self.ship_fee
        return int(self.tax_percent*sum/100.0)

    def lines_total(self):
        sum=0
        for li in self.invoice_lines():
            sum+=int(li.quantity*li.unit_price)
        return sum
    def sum_total(self):
        sum=self.lines_total()
        sum+=self.ship_fee
        sum+=self.tax_amount()
        sum-=self.discount
        return sum
    def save(self,*args, **kwargs):
        if self.class_name is None:
            self.class_name='invoice' 
        if self.app_name is None:
            self.app_name=APP_NAME
        if self.title is None or self.title=="":
            self.title=f"فاکتور شماره {self.pk}"
        self.amount=self.sum_total()
        super(Invoice,self).save(*args, **kwargs)
      
    class Meta:
        verbose_name = _("Invoice")
        verbose_name_plural = _("Invoices")
    
    def __str__(self):
        from utility.currency import to_price
        return f"""{self.title}   ({to_price(self.sum_total())}) """
   
    def invoice_lines(self):
        return InvoiceLine.objects.filter(invoice=self).order_by('row')
    def get_edit_url2(self):
        return reverse(APP_NAME+":edit_invoice",kwargs={'pk':self.pk})


class InvoiceLine(models.Model):
    date_added=models.DateTimeField(_("date_added"), auto_now=False, auto_now_add=True)
    invoice=models.ForeignKey("invoice",blank=True, verbose_name=_("invoice"),related_name="lines", on_delete=models.CASCADE)
    row=models.IntegerField(_("row"),blank=True)
    product_or_service=models.ForeignKey("productorservice", verbose_name=_("productorservice"), on_delete=models.CASCADE)
    quantity=models.FloatField(_("quantity"))
    unit_price=models.IntegerField(_("unit_price"))
    unit_name=models.CharField(_("unit_name"),max_length=50,choices=UnitNameEnum.choices,default=UnitNameEnum.ADAD)
    description=models.CharField(_("description"),null=True,blank=True, max_length=50)
    def save(self,*args, **kwargs):
        super(InvoiceLine,self).save(*args, **kwargs)
        self.invoice.save()
    class Meta:
        verbose_name = _("InvoiceLine")
        verbose_name_plural = _("InvoiceLines")

    def __str__(self):
        return f"{self.invoice} {self.row} - {self.product_or_service.title} "

    def get_absolute_url(self):
        return reverse("InvoiceLine_detail", kwargs={"pk": self.pk})

  
class Spend(Transaction,LinkHelper):    
    spend_type=models.CharField(_("spend_type"),choices=SpendTypeEnum.choices, max_length=50)
    class_name="spend"
    
    class Meta:
        verbose_name = _("Spend")
        verbose_name_plural = _("Spends")
    def color(self):
        color='primary'
        if self.spend_type==SpendTypeEnum.COST:
            color="danger"
        if self.spend_type==SpendTypeEnum.WAGE:
            color="success"
        return color

    def save(self,*args, **kwargs):
        super(Spend,self).save(*args, **kwargs)
   

class Payment(Transaction):
    class Meta:
        verbose_name = _("Payment")
        verbose_name_plural = _("پرداخت ها")

    def save(self,*args, **kwargs):
        if self.app_name is None:
            self.app_name=APP_NAME 
        if self.class_name is None:
            self.class_name='payment' 
        if self.transaction_datetime is None:
            self.transaction_datetime=timezone.now()
        super(Payment,self).save(*args, **kwargs)
        


class Salary(Spend,LinkHelper):    
    class_name="wage"
    month=models.IntegerField(_("month"))
    year=models.IntegerField(_("year"))
    def month_year(self):
        return PERSIAN_MONTH_NAMES[self.month-1]+" " + str(self.year)
    
    class Meta:
        verbose_name = _("Salary")
        verbose_name_plural = _("Salaries")
   
    def save(self,*args, **kwargs):
        if self.class_name is None or self.class_name=="":
            self.class_name='wage'
        if self.app_name is None or self.app_name=="":
            self.app_name=APP_NAME
        super(Salary,self).save(*args, **kwargs)
        for fd in self.financialdocument_set.all():
            FinancialBalance.objects.filter(financial_document=fd).delete()
            fb=FinancialBalance(financial_document=fd)
            fb.wage=self.amount
            fb.save()

            
class Cost(Spend,LinkHelper):    
    cost_type=models.CharField(_("cost"),choices=CostTypeEnum.choices, max_length=50)
    class_name="cost"
    def color(self):
        color='primary'
        if self.cost_type==CostTypeEnum.WATER:
            color="info"
        if self.cost_type==CostTypeEnum.INTERNET:
            color="success"
        if self.cost_type==CostTypeEnum.TRANSPORT:
            color="danger"
        if self.cost_type==CostTypeEnum.ELECTRICITY:
            color="primary"
        if self.cost_type==CostTypeEnum.TELEPHONE:
            color="secondary"
        if self.cost_type==CostTypeEnum.GAS:
            color="danger"
        return color
    
    class Meta:
        verbose_name = _("Cost")
        verbose_name_plural = _("Costs")

   
    def save(self,*args, **kwargs):
        if self.class_name is None or self.class_name=="":
            self.class_name='cost'
        if self.app_name is None or self.app_name=="":
            self.app_name=APP_NAME
        super(Cost,self).save(*args, **kwargs)
        for fd in self.financialdocument_set.all():
            FinancialBalance.objects.filter(financial_document=fd).delete()
            fb=FinancialBalance(financial_document=fd)
            fb.cost=self.amount
            fb.save()
