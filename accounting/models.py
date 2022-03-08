from core.middleware import get_request
from unicodedata import category
from django.db import models
from django.forms import CharField
from core.models import Page
from django.shortcuts import reverse
from django.utils.translation import gettext as _
from .apps import APP_NAME
from utility.utils import LinkHelper
from .enums import *
from tinymce.models import HTMLField
from core.enums import ColorEnum,UnitNameEnum


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
        super(Transaction,self).save(*args, **kwargs)
        FinancialDocument.objects.filter(transaction=self).delete()
        fd=FinancialDocument(transaction=self,account_id=self.pay_to.id)
        fd.save()
        fd=FinancialDocument(transaction=self,account_id=self.pay_from.id)
        fd.save()

 
class ProductorService(Page):

    
    @property
    def unit_price(self):
        return 0
    @property
    def unit_name(self):
        return "عدد"

    class Meta:
        verbose_name = _("ProductorService")
        verbose_name_plural = _("ProductorServices")


class Product(ProductorService):

    class Meta:
        verbose_name = _("Product")
        verbose_name_plural = _("Products")






    @property
    def available(self):
        return 0
        
    def save(self,*args, **kwargs):
        if self.class_name is None or self.class_name=="":
            self.class_name='product'
        if self.app_name is None or self.app_name=="":
            self.app_name=APP_NAME
        return super(Product,self).save(*args, **kwargs)

 
class Service(ProductorService):

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
    title=models.CharField(_("title"), null=True,blank=True,max_length=500)
    profile=models.ForeignKey("authentication.profile", verbose_name=_("profile"), on_delete=models.CASCADE)
    class_name="account"
    app_name=APP_NAME

    class Meta:
        verbose_name = _("Account")
        verbose_name_plural = _("Accounts")

    def __str__(self):
        return self.title

    def save(self,*args, **kwargs):
        if self.title is None or self.title=="":
            self.title=self.profile.name
        super(Account,self).save(*args, **kwargs)


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


class FinancialDocument(models.Model,LinkHelper):
    account=models.ForeignKey("account", verbose_name=_("account"), on_delete=models.CASCADE)
    transaction=models.ForeignKey("transaction",verbose_name=_("transaction"), on_delete=models.CASCADE)
    tags=models.ManyToManyField("FinancialDocumentTag", blank=True,verbose_name=_("tags"))
    @property
    def rest(self):
        rest=0
        for fd in FinancialDocument.objects.filter(account=self.account).filter(transaction__transaction_datetime__lte=self.transaction.transaction_datetime):
            rest+=fd.bestankar
            rest-=fd.bedehkar
        return rest
    
    @property
    def bedehkar(self):
        a=0
        if self.transaction.pay_to.id==self.account.id:
            a=self.transaction.amount
        return a
    @property
    def title(self):
        return self.transaction.title 
     
    @property
    def bestankar(self):
        a=0
        if self.transaction.pay_from.id==self.account.id:
            a=self.transaction.amount
        return a
    class_name="financialdocument"
    app_name=APP_NAME
    

    class Meta:
        verbose_name = _("FinancialDocument")
        verbose_name_plural = _("FinancialDocuments")

    def __str__(self):
        return f"""{self.account.title} : {self.transaction.title} : {self.transaction.amount}"""

    def save(self):
        super(FinancialDocument,self).save()
        (fb,res)=FinancialBalance.objects.get_or_create(financial_document=self)


class FinancialBalance(models.Model,LinkHelper):
    class_name="financialbalance"
    app_name=APP_NAME
    financial_document=models.ForeignKey("FinancialDocument", verbose_name=_("FinancialDocument"), on_delete=models.CASCADE)
    sell_benefit=models.IntegerField(_("سود حاصل از فروش"),default=0)
    sell_loss=models.IntegerField(_("زیان حاصل از فروش"),default=0)
    cost=models.IntegerField(_("هزینه"),default=0)
    tax=models.IntegerField(_("مالیات"),default=0)
    wage=models.IntegerField(_("حقوق"),default=0)
    sell_service=models.IntegerField(_("فروش خدمات"),default=0)
    buy_service=models.IntegerField(_("خرید خدمات"),default=0)
    discount=models.IntegerField(_("تخفیف"),default=0)
    ship_fee=models.IntegerField(_("هزینه حمل"),default=0)
    
    def sum(self):
        sum=0
        sum+=self.sell_benefit
        sum+=self.sell_loss
        sum+=self.cost
        sum+=self.tax
        sum+=self.wage
        sum+=self.sell_service
        sum+=self.discount
        sum+=self.ship_fee
        return sum
    class Meta:
        verbose_name = _("FinancialBalance")
        verbose_name_plural = _("FinancialBalances")

    def __str__(self):
        return self.financial_document.title 


class Payment(Transaction):
    


        
    class Meta:
        verbose_name = _("Payment")
        verbose_name_plural = _("Payments")

    def save(self,*args, **kwargs):
        self.class_name="payment"
        super(Payment,self).save(*args, **kwargs)
        financial_year=FinancialYear.get_by_date(date=self.transaction_datetime)
        category,aa=FinancialDocumentCategory.objects.get_or_create(title="واریز")
        FinancialDocument.objects.filter(transaction=self).delete()

        ifd1=FinancialDocument()
        ifd1.financial_year=financial_year
        ifd1.category=category
        ifd1.account=self.pay_to
        ifd1.transaction=self
        ifd1.bedehkar=self.amount
        ifd1.title=str(self)
        ifd1.document_datetime=self.transaction_datetime
        ifd1.save()

        ifd1=FinancialDocument()
        ifd1.bestankar=self.amount
        ifd1.transaction=self
        ifd1.title=str(self)
        ifd1.financial_year=financial_year
        ifd1.category=category
        ifd1.document_datetime=self.transaction_datetime
        ifd1.account=self.pay_from
        ifd1.save()


class FinancialDocumentTag(models.Model):
    title=models.CharField(_("title"), max_length=50)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'FinancialDocumentTag'
        verbose_name_plural = 'FinancialDocumentTags'

class Cheque(Transaction,LinkHelper):
    cheque_date=models.DateField(_("تاریخ چک"), auto_now=False, auto_now_add=False)
    def persian_cheque_date(self):
        return PersianCalendar().from_gregorian(self.cheque_date)

    class_name="cheque"
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
        self.class_name="cheque"
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
    
    def editable(self):
        if self.status==TransactionStatusEnum.DRAFT:
            return True
        if self.status==TransactionStatusEnum.IN_PROGRESS:
            return True
        return False
    def get_title(self):
        return self.title or f"فاکتور شماره {self.pk}"
    @property
    def customer(self):
        return self.pay_to
    @property
    def seller(self):
        return Store.objects.filter(pk=self.pay_from.pk).first()


    def get_edit_url2(self):
        return reverse(APP_NAME+":edit_invoice",kwargs={'pk':self.pk})
    def get_print_url(self):
        return reverse(APP_NAME+":invoice_print",kwargs={'pk':self.pk})
    # @property
    # def title(self):
    #     try:

    #         return "فاکتور شماره "+str(self.pk)
    #     except:
    #         return "فاکتور شماره 0"
    def persian_invoice_datetime(self):
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
        sum+=((sum*self.tax_percent)/100.0)
        sum-=self.discount
        return sum
    def save(self,*args, **kwargs):
        
        super(Invoice,self).save(*args, **kwargs)
        self.class_name='invoice'
        if self.title is None or self.title=="":
            self.title=f"فاکتورشماره {self.pk}"
            self.save()
      
    class Meta:
        verbose_name = _("Invoice")
        verbose_name_plural = _("Invoices")
    
    def __str__(self):
        from utility.currency import to_price
        return f"""{self.title}   ({to_price(self.sum_total())}) """
   
    def invoice_lines(self):
        return InvoiceLine.objects.filter(invoice=self).order_by('row')


class InvoiceLine(models.Model):
    invoice=models.ForeignKey("invoice", verbose_name=_("invoice"),related_name="lines", on_delete=models.CASCADE)
    row=models.IntegerField(_("row"))
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


class WareHouse(Page):
    # store=models.ForeignKey("store",related_name="ware_houses", verbose_name=_("store"), on_delete=models.CASCADE)
    address=models.CharField(_("address"),null=True,blank=True, max_length=50)
    tel=models.CharField(_("tel"),null=True,blank=True, max_length=50)
    owner=models.ForeignKey("account", verbose_name=_("owner"), on_delete=models.CASCADE)
    def get_print_url(self):
        return reverse(APP_NAME+":ware_house_print",kwargs={'pk':self.pk})

    class Meta:
        verbose_name = _("WareHouse")
        verbose_name_plural = _("WareHouses")

    def save(self,*args, **kwargs):
        self.class_name="warehouse"
        return super(WareHouse,self).save(*args, **kwargs)


class Guarantee(models.Model,LinkHelper):
    invoice=models.ForeignKey("invoice", verbose_name=_("فاکتور"), on_delete=models.CASCADE)
    product=models.ForeignKey("product", verbose_name=_("کالا"), on_delete=models.CASCADE)
    start_date=models.DateField(_("شروع گارانتی"), auto_now=False, auto_now_add=False)
    end_date=models.DateField(_("پابان گارانتی"), auto_now=False, auto_now_add=False)
    status=models.CharField(_("وضعیت"),choices=GuaranteeStatusEnum.choices,default=GuaranteeStatusEnum.VALID, max_length=50)
    type=models.CharField(_("نوع گارانتی"),choices=GuaranteeTypeEnum.choices,default=GuaranteeTypeEnum.REPAIR, max_length=50)
    serial_no=models.CharField(_("شماره سریال"), max_length=50)
    conditions=models.CharField(_("شرایط"),null=True,blank=True, max_length=5000)
    description=HTMLField(_("توضیحات"),null=True,blank=True, max_length=50000)
    class_name="guarantee"    
    def persian_end_date(self):
        return PersianCalendar().from_gregorian(self.end_date)
    def persian_start_date(self):
        return PersianCalendar().from_gregorian(self.start_date)
    class Meta:
        verbose_name = _("Guarantee")
        verbose_name_plural = _("Guarantees")
            

class WareHouseSheet(models.Model,LinkHelper):
    date_added=models.DateTimeField(_("date_added"), auto_now=False, auto_now_add=True)
    date_registered=models.DateTimeField(_("date_registered"), auto_now=False, auto_now_add=False)
    creator=models.ForeignKey("authentication.profile", verbose_name=_("creator"), on_delete=models.CASCADE)    
    invoice=models.ForeignKey("invoice", verbose_name=_("invoice"), on_delete=models.CASCADE)    
    product=models.ForeignKey("product", verbose_name=_("product"), on_delete=models.CASCADE)    
    quantity=models.IntegerField(_("quantity"))
    unit_name=models.CharField(_("unit_name"),choices=UnitNameEnum.choices,default=UnitNameEnum.ADAD, max_length=50)
    direction=models.CharField(_("direction"),choices=WareHouseSheetDirectionEnum.choices, max_length=50)
    ware_house=models.ForeignKey("warehouse", verbose_name=_("ware_house"), on_delete=models.CASCADE)
    status=models.CharField(_("status"),choices=WareHouseSheetStatusEnum.choices,default=WareHouseSheetStatusEnum.INITIAL, max_length=50)
    description=HTMLField(_("description"),null=True,blank=True,max_length=50000)
    class_name="warehousesheet"
    class Meta:
        verbose_name = _("WareHouseSheet")
        verbose_name_plural = _("WareHouseSheets")
    def persian_date_registered(self):
        return PersianCalendar().from_gregorian(self.date_registered)

    def save(self,*args, **kwargs):
        self.class_name="warehousesheet"
        super(WareHouseSheet,self).save(*args, **kwargs)
    def available(self):
        a=0;
        for aa in WareHouseSheet.objects.filter(ware_house=self.ware_house).filter(product=self.product).filter(status=WareHouseSheetStatusEnum.DONE):
            if aa.direction==WareHouseSheetDirectionEnum.IMPORT:
                a+=aa.quantity
            if aa.direction==WareHouseSheetDirectionEnum.EXPORT:
                a-=aa.quantity
        return a
    def color(self):
        color="primary"
        if self.direction==WareHouseSheetDirectionEnum.IMPORT:
            color="success"
        if self.direction==WareHouseSheetDirectionEnum.EXPORT:
            color="danger"
        return color


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


class Wage(Spend,LinkHelper):    
    class_name="wage"
    month=models.IntegerField(_("month"))
    year=models.IntegerField(_("year"))
    def month_year(self):
        return PERSIAN_MONTH_NAMES[self.month-1]+" " + str(self.year)
    
    class Meta:
        verbose_name = _("Wage")
        verbose_name_plural = _("Wages")

   
    def save(self,*args, **kwargs):
        if self.class_name is None or self.class_name=="":
            self.class_name='wage'
        if self.app_name is None or self.app_name=="":
            self.app_name=APP_NAME
        super(Wage,self).save(*args, **kwargs)
        for fd in self.financialdocument_set.all():
            FinancialBalance.objects.filter(financial_document=fd).delete()
            fb=FinancialBalance(financial_document=fd)
            fb.wage=self.amount
            fb.save()
            