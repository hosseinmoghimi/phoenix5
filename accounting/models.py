from authentication.models import IMAGE_FOLDER
from core.enums import ColorEnum, UnitNameEnum,BS_ColorCode
from core.middleware import get_request
from core.models import Color, ImageMixin, Page
from django.db import models
from django.shortcuts import reverse
from django.utils import timezone
from django.utils.translation import gettext as _
from phoenix.server_settings import STATIC_URL
from phoenix.settings import MEDIA_URL
from tinymce.models import HTMLField
from utility.calendar import (PERSIAN_MONTH_NAMES, PersianCalendar,
                              to_persian_datetime_tag)
from utility.currency import to_price
from utility.excel import get_excel_report
from utility.log import leolog
from utility.utils import LinkHelper

from accounting.apps import APP_NAME
from accounting.enums import *


class Asset(Page,LinkHelper):

    price=models.IntegerField(_("price"),default=0)
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
    pay_from=models.ForeignKey("account",related_name="transactions_from", verbose_name=_("پرداخت کننده"), on_delete=models.PROTECT)
    pay_to=models.ForeignKey("account", related_name="transactions_to",verbose_name=_("دریافت کننده"), on_delete=models.PROTECT)
    creator=models.ForeignKey("authentication.profile",null=True,blank=True, verbose_name=_("ثبت شده توسط"), on_delete=models.SET_NULL)
    status=models.CharField(_("وضعیت"),choices=TransactionStatusEnum.choices,default=TransactionStatusEnum.DRAFT, max_length=50)
    category=models.ForeignKey("transactioncategory",null=True,blank=True, verbose_name=_("دسته بندی"), on_delete=models.SET_NULL)
    amount=models.IntegerField(_("مبلغ"),default=0)
    payment_method=models.CharField(_("نوع پرداخت"),choices=PaymentMethodEnum.choices,default=PaymentMethodEnum.DRAFT, max_length=50)
    transaction_datetime=models.DateTimeField(_("تاریخ تراکنش"), auto_now=False, auto_now_add=False)
    print_datetime=models.DateTimeField(_("تاریخ چاپ"),null=True,blank=True, auto_now=False, auto_now_add=False)
    def add_print_event(self,*args, **kwargs):
        from django.utils import timezone
        self.print_datetime=timezone.now()
        super(Transaction,self).save()

    def status_color(self):
        return self.color()
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
    def payment_method_color(self):
        color="primary"
        if self.payment_method==PaymentMethodEnum.CARD:
            color="primary"
        if self.payment_method==PaymentMethodEnum.PRODUCT:
            color="danger"
        if self.payment_method==PaymentMethodEnum.SERVICE:
            color="success"
        if self.payment_method==PaymentMethodEnum.MOBILE_BANK:
            color="warning"
        if self.payment_method==PaymentMethodEnum.IN_CASH:
            color="warning"
        if self.payment_method==PaymentMethodEnum.POS:
            color="warning"
        if self.payment_method==PaymentMethodEnum.CARD:
            color="secondary"
        return color
    class Meta:
        verbose_name = _("Transaction")
        verbose_name_plural = _("Transactions")

    def __str__(self):
        return f"{self.title} ({self.status})"

    def roll_back(self,*args, **kwargs):
        self.status=TransactionStatusEnum.ROLL_BACKED
        super(Transaction,self).save(*args, **kwargs)


    def save(self,*args, **kwargs):
        if self.transaction_datetime is None:
            self.transaction_datetime=PersianCalendar().date
        super(Transaction,self).save(*args, **kwargs)
        if self.status==TransactionStatusEnum.DRAFT or self.status==TransactionStatusEnum.CANCELED:
            financial_documents=FinancialDocument.objects.filter(transaction=self)
            for fd in financial_documents:
                fd.status=self.status
                fd.save()
        else:
        # if True:
            fd_bedehkar=FinancialDocument.objects.filter(transaction=self).filter(account_id=self.pay_to.id).first()
            FinancialDocument.objects.filter(transaction=self).exclude(account_id=self.pay_from.id).filter(bedehkar=self.amount).delete()
            if fd_bedehkar is None:
                fd_bedehkar=FinancialDocument(transaction=self,account_id=self.pay_to.id,direction=FinancialDocumentDirectionEnum.BEDEHKAR)
            fd_bedehkar.account_id=self.pay_to.id
            fd_bedehkar.status=self.status
            fd_bedehkar.bestankar=0
            fd_bedehkar.bedehkar=self.amount
            fd_bedehkar.save()

            fd_bestankar=FinancialDocument.objects.filter(transaction=self).filter(account_id=self.pay_from.id).first()
            FinancialDocument.objects.filter(transaction=self).exclude(account_id=self.pay_from.id).filter(bestankar=self.amount).delete()
            if fd_bestankar is None:
                fd_bestankar=FinancialDocument(transaction=self,account_id=self.pay_from.id,direction=FinancialDocumentDirectionEnum.BESTANKAR)
            fd_bestankar.account_id=self.pay_from.id
            fd_bestankar.status=self.status
            fd_bestankar.bestankar=self.amount
            fd_bestankar.bedehkar=0
            fd_bestankar.save()

    @property
    def persian_transaction_datetime(self,no_tag=False,*args, **kwargs):
        if no_tag:
            return PersianCalendar().from_gregorian(self.transaction_datetime)
        return to_persian_datetime_tag(self.transaction_datetime)

    @property
    def editable(self):
        old_transaction=Transaction.objects.filter(pk=self.pk).first()
        if old_transaction is None:
            return True
        if old_transaction.status==TransactionStatusEnum.ROLL_BACKED:
            return True
        if old_transaction.status==TransactionStatusEnum.FROM_PAST:
            return True
        if old_transaction.status==TransactionStatusEnum.READY:
            return False
        if old_transaction.status==TransactionStatusEnum.CANCELED:
            return True
        if old_transaction.status==TransactionStatusEnum.FINISHED:
            return False
        if old_transaction.status==TransactionStatusEnum.PASSED:
            return False
        if old_transaction.status==TransactionStatusEnum.DELIVERED:
            return False
        if old_transaction.status==TransactionStatusEnum.DRAFT:
            return True
        if old_transaction.status==TransactionStatusEnum.IN_PROGRESS:
            return True
        return False


class DoubleTransaction(Page): 
    # employer_transaction_id=models.IntegerField(_("employer_transaction_id"),default=0)
    # middle_transaction_id=models.IntegerField(_("middle_transaction_id"),default=0)
    employer_transaction=models.ForeignKey("transaction", related_name="employer_transaction_set",verbose_name=_("employer_transaction"),null=True,blank=True, on_delete=models.SET_NULL)
    middle_transaction=models.ForeignKey("transaction", related_name="middle_transaction_set",verbose_name=_("middle_transaction"),null=True,blank=True, on_delete=models.SET_NULL)
    # employer=models.ForeignKey("account", related_name="double_transaction_employer_set",verbose_name=_("employer"), on_delete=models.CASCADE)
    # middle=models.ForeignKey("account", related_name="double_transaction_middle_set",verbose_name=_("middle"), on_delete=models.CASCADE)
    # contractor=models.ForeignKey("account", related_name="double_transaction_contractor_set",verbose_name=_("contractor"), on_delete=models.CASCADE)
    # employer_paid=models.IntegerField(_("employer_paid"))
    # middle_paid=models.IntegerField(_("middle_paid"))
    # date_added=models.DateTimeField(_("date_added"), auto_now=False, auto_now_add=True)
    # employer_transaction_date_time=models.DateTimeField(_("date_added"), auto_now=False, auto_now_add=False)
    # middle_transaction_date_time=models.DateTimeField(_("date_added"), auto_now=False, auto_now_add=False)
    # @property
    # def employer_transaction(self):
        # return Transaction.objects.filter(pk=self.employer_transaction_id).first()
    # @property
    # def middle_transaction(self):
        # return Transaction.objects.filter(pk=self.middle_transaction_id).first()

    class Meta:
        verbose_name = _("DoubleTransaction")
        verbose_name_plural = _("DoubleTransactions")

    def save(self,*args, **kwargs):
        if self.app_name is None or self.app_name=="":
            self.app_name=APP_NAME
        if self.class_name is None or self.class_name=="":
            self.class_name="doubletransaction"


        # if self.employer_transaction is None:
            # employer_transaction=Transaction()
        super(DoubleTransaction,self).save()


class ProductOrService(Page):
    barcode=models.CharField(_("بارکد"),null=True,blank=True, max_length=100)

    def get_market_absolute_url(self):
        return reverse("market:product",kwargs={'pk':self.pk})
 
    def unit_names(self):
        unit_names=ProductOrServiceUnitName.objects.filter(product_or_service_id=self.pk)
        if len(unit_names)==0:
            product_or_service_unit_name=ProductOrServiceUnitName()
            product_or_service_unit_name.product_or_service_id=self.pk
            product_or_service_unit_name.unit_name=UnitNameEnum.ADAD
            product_or_service_unit_name.save()
            return [product_or_service_unit_name]
        return unit_names

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
        
        request=get_request()
        if request is not None:
             
            account=Account.objects.filter(profile__user_id=request.user.id).first()
            last_price=Price.objects.filter(buy_price__gt=0).filter(product_or_service=self).filter(account=account).order_by("-date_added").first()
            if last_price is not None:
                return last_price.unit_name
        return "عدد"

    class Meta:
        verbose_name = _("ProductOrService")
        verbose_name_plural = _("ProductOrServices")

    @property
    def category(self):
        return self.category_set.first()

    def save(self,*args, **kwargs):
        super(ProductOrService,self).save()
        unit_names=ProductOrServiceUnitName.objects.filter(product_or_service_id=self.pk)
        if len(unit_names)==0:
            product_or_service_unit_name=ProductOrServiceUnitName()
            product_or_service_unit_name.product_or_service_id=self.pk
            product_or_service_unit_name.unit_name=UnitNameEnum.ADAD
            product_or_service_unit_name.save()

    @property
    def image(self):
        return self.thumbnail


class ProductOrServiceUnitName(models.Model,LinkHelper):
    product_or_service=models.ForeignKey("productorservice", verbose_name=_("productorservice"), on_delete=models.CASCADE)
    unit_name=models.CharField(_("unit_name"),max_length=50,choices=UnitNameEnum.choices,default=UnitNameEnum.ADAD)
    coef=models.IntegerField(_("coef"),default=1)
    app_name=APP_NAME
    class_name="productorserviceunitname"
    

    class Meta:
        verbose_name = _("ProductOrServiceUnitName")
        verbose_name_plural = _("ProductOrServiceUnitNames")

    def __str__(self):
        return f"{self.product_or_service.title} {self.unit_name}"


class Product(ProductOrService):
    # specifications=models.ManyToManyField("ProductSpecification", verbose_name=_("ویژگی ها"))

    class Meta:
        verbose_name = _("Product")
        verbose_name_plural = _("Products")


    def get_pm_absolute_url(self):
        return reverse('projectmanager:material',kwargs={'pk':self.pk})

 
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
    def get_market_absolute_url(self):
        return reverse("market:product",kwargs={'pk':self.pk})
 

class AccountTag(models.Model,LinkHelper):
    account=models.ForeignKey("account", verbose_name=_("account"), on_delete=models.CASCADE)
    tag=models.CharField(_("tag"), max_length=50)
    app_name=APP_NAME
    class_name="accounttag"
    class Meta:
        verbose_name = _("AccountTag")
        verbose_name_plural = _("AccountTags")

    def __str__(self):
        return self.account.title +" " +self.tag
 

class Service(ProductOrService):

    class Meta:
        verbose_name = _("Service")
        verbose_name_plural = _("Services")
 
    def get_pm_absolute_url(self):
        return reverse('projectmanager:service',kwargs={'pk':self.pk})

    def save(self,*args, **kwargs):
        if self.class_name is None or self.class_name=="":
            self.class_name='service'
        if self.app_name is None or self.app_name=="":
            self.app_name=APP_NAME
        return super(Service,self).save(*args, **kwargs)


class ProductSpecification(models.Model,LinkHelper):
    product=models.ForeignKey("product", verbose_name=_("product"), on_delete=models.CASCADE)
    name=models.CharField(_("name"), max_length=200)
    value=models.CharField(_("value"), max_length=200)
    app_name=APP_NAME
    class_name="productspecification"
    
    class Meta:
        verbose_name = _("ProductSpecification")
        verbose_name_plural = _("ProductSpecifications")

    def __str__(self):
        return f"{self.product.title}:{self.name}:{self.value}"


class Account(models.Model,LinkHelper):
    logo_origin=models.ImageField(_("لوگو , تصویر"), null=True,blank=True,upload_to=IMAGE_FOLDER+"account/", height_field=None, width_field=None, max_length=None)
    title=models.CharField(_("عنوان"), null=True,blank=True,max_length=500)
    profile=models.ForeignKey("authentication.profile", verbose_name=_("profile"),null=True,blank=True, on_delete=models.CASCADE)
    address=models.CharField(_("آدرس"),null=True,blank=True, max_length=200)
    tel=models.CharField(_("تلفن"),null=True,blank=True, max_length=50)
    mobile=models.CharField(_("موبایل"),null=True,blank=True, max_length=50)
    description=models.CharField(_("توضیحات"),blank=True,max_length=5000)
    economic_no=models.CharField(_("شماره اقتصادی"),max_length=50,null=True,blank=True)
    melli_id=models.CharField(_("شناسه ملی"),max_length=50,null=True,blank=True)
    register_no=models.CharField(_("شماره ثبت"),max_length=50,null=True,blank=True)
    fax=models.CharField(_("شماره فکس"),max_length=50,null=True,blank=True)
    postal_code=models.CharField(_("کد پستی"),max_length=50,null=True,blank=True)
    priority=models.IntegerField(_("priority"),default=1000)
    class_name=models.CharField(_("class_name"),blank=True, max_length=50)
    app_name=models.CharField(_("app_name"),blank=True,max_length=50)
    def default_bank_account(self):
        return BankAccount.default_bank_account(account_id=self.id)
    def get_whatsapp_link(self):
        if self.tel is not None:
            from utility.share import whatsapp_link
            return whatsapp_link(self.tel)  
    @property
    def class_title(self):
        class_title="حساب مالی"
        if self.class_name=="client":
            class_title="سرویس گیرنده رفت و آمد"
        if self.class_name=="account":
            class_title="حساب مالی"
        if self.class_name=="driver":
            class_title="راننده"
        if self.class_name=="passenger":
            class_title="مسافر"
        if self.class_name=="serviceman":
            class_title="سرویس کار"
        return class_title
    def balance_rest(self):
        bestankar=0
        bedehkar=0
        for doc in self.financialdocument_set.all():
            bestankar+=doc.bestankar
            bedehkar+=doc.bedehkar
        balance_rest=bestankar-bedehkar
        return balance_rest

    def invoices(self):
        return Invoice.objects.filter(models.Q(pay_from=self)|models.Q(pay_to=self))

    def logo(self):
        if self.logo_origin:
            return MEDIA_URL+str(self.logo_origin)
        if self.profile is not None:
            return self.profile.image
        return f"{STATIC_URL}{self.app_name}/img/{self.class_name}.png"
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
        if self.class_name is None or self.class_name=="":
            self.class_name='account'
        if self.app_name is None or self.app_name=="":
            self.app_name=APP_NAME
            
        # from projectmanager.models import Employee
        # a=Account.objects.filter(fff="")
        if self.title is None or self.title=="":
            if self.profile is not None:
                self.title=self.profile.name 
        super(Account,self).save(*args, **kwargs)
    
    @property
    def balance(self):
        balance={}
        bestankar=0
        bedehkar=0
        for doc in self.financialdocument_set.all():
            if doc.status==FinancialDocumentStatusEnum.DRAFT or  doc.status==FinancialDocumentStatusEnum.CANCELED or  doc.status==FinancialDocumentStatusEnum:
                pass
            else:
                bestankar+=doc.bestankar
                bedehkar+=doc.bedehkar
        rest=bestankar-bedehkar
        balance['rest']=rest
        balance['bestankar']=bestankar
        balance['bedehkar']=bedehkar
        return balance


class Bank(models.Model,LinkHelper):
    name=models.CharField(_("بانک"), max_length=50)
    branch=models.CharField(_("شعبه"),null=True,blank=True, max_length=50)
    address=models.CharField(_("آدرس"),null=True,blank=True, max_length=50)
    tel=models.CharField(_("تلفن"),null=True,blank=True, max_length=50)
    class_name="bank"
    app_name=APP_NAME
    @property
    def logo(self):
        return ""
    
    @property
    def title(self):
        return self.name
    
    def __str__(self):
        a=f"""{self.name}"""
        if self.branch is not None:
            a+=" شعبه "+self.branch 
        return a


    class Meta:
        verbose_name = _("Bank")
        verbose_name_plural = _("Banks")


class BankAccount(models.Model,LinkHelper):
    title=models.CharField(_("title"),blank=True, max_length=50)
    account=models.ForeignKey("account", verbose_name=_("account"), on_delete=models.CASCADE)
    bank=models.ForeignKey("bank", verbose_name=_("bank"), on_delete=models.CASCADE)
    account_no=models.CharField(_("شماره حساب"),null=True,blank=True, max_length=50)
    card_no=models.CharField(_("شماره کارت"),null=True,blank=True, max_length=50)
    shaba_no=models.CharField(_("شماره شبا"),null=True,blank=True, max_length=50)
    is_defult=models.BooleanField(_("default"),default=False)
    class_name='bankaccount'
    app_name=APP_NAME

    def default_bank_account(account_id):
        if account_id is None or account_id<1:
            return
        all_bank_account=BankAccount.objects.filter(account_id=account_id)
        bank_account=all_bank_account.filter(is_defult=True).first()
        if bank_account is not None:
            return bank_account
        return all_bank_account.first()

    class Meta:
        verbose_name = _("BankAccount")
        verbose_name_plural = _("BankAccounts")

    # def balance(self):
    #     return 0-self.rest()
 
    def __str__(self):
        return f"حساب {self.bank} {self.account} {self.account} : {self.title}"

    def save(self,*args, **kwargs):
         
        # from projectmanager.models import Employee
        # a=Account.objects.filter(fff="")
        if self.title is None or self.title=="":
            account_name=""
            if self.account is not None:
                account_name=self.account.title 
            self.title=f"""حساب {self.bank} {account_name}"""
        super(BankAccount,self).save(*args, **kwargs)
    
    def to_variz_text(bank_account):
        if bank_account is None:
            return ""
        text=" جهت واریز : "
        if bank_account.account_no:
            text+="""<small class="text-muted"> شماره حساب : </small>"""
            text+=bank_account.account_no
        if bank_account.card_no:
            text+="""<small class="text-muted"> شماره کارت :</small> """
            text+=bank_account.card_no
        if bank_account.shaba_no:
            text+="""<small class="text-muted"> شماره شبا :</small>"""
            text+=bank_account.shaba_no
        if bank_account.account:
            text+="""<small class="text-muted"> به نام  : </small>"""
            text+= bank_account.title
        return f"""<span class="rtl farsi">{text}</span>"""


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
    account=models.ForeignKey("account", verbose_name=_("account"), on_delete=models.PROTECT)
    bedehkar=models.IntegerField(_("bedehkar"),default=0)
    bestankar=models.IntegerField(_("bestankar"),default=0)
    transaction=models.ForeignKey("transaction",verbose_name=_("transaction"), on_delete=models.CASCADE)
    tags=models.ManyToManyField("FinancialDocumentTag", blank=True,verbose_name=_("tags"))
    color=models.CharField(_("color"),max_length=50,choices=ColorEnum.choices,default=ColorEnum.PRIMARY)
    direction=models.CharField(_("direction"),max_length=50,choices=FinancialDocumentDirectionEnum.choices,default=FinancialDocumentDirectionEnum.BESTANKAR)
    status=models.CharField(_("status"),choices=FinancialDocumentStatusEnum.choices,default=FinancialDocumentStatusEnum.APPROVED, max_length=50)
    app_name=APP_NAME
    class_name="financialdocument"

    @property
    def rest(self):
        rest=0
        rest_=0
        fds=FinancialDocument.objects.filter(account=self.account)
        fds=fds.filter(transaction__transaction_datetime__lte=self.transaction.transaction_datetime)
        
        for fd in fds :
            if self.pk==fd.pk:
                # break
                pass
            rest+=fd.bestankar
            rest-=fd.bedehkar
            rest_=rest

        # rest_+=self.bestankar
        # rest_-=self.bedehkar

        # print(self.bedehkar,self.bestankar,rest_)
        return rest_
    def status_color(self):
        color="primary"
        if self.status==FinancialDocumentStatusEnum.DRAFT:
            color="secondary"
        if self.status==FinancialDocumentStatusEnum.APPROVED:
            color="success"
        if self.status==FinancialDocumentStatusEnum.IN_PROGRESS:
            color="warning"
        if self.status==FinancialDocumentStatusEnum.CANCELED:
            color="secondary"
        return color
    def get_state_badge(self):
        color="muted"
        state="تسویه"
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
            return PersianCalendar().from_gregorian(self.transaction.transaction_datetime)
        return to_persian_datetime_tag(self.transaction.transaction_datetime)
    @property
    def title(self):
        return self.transaction.title 
     
    def normalize_sub_accounts(self):
        sum_bestankar=0
        sum_bedehkar=0
        financial_balances=FinancialBalance.objects.filter(financial_document_id=self.pk)
        for financialbalance in financial_balances.exclude(title=FinancialBalanceTitleEnum.MISC):
            sum_bedehkar+=financialbalance.bedehkar
            sum_bestankar+=financialbalance.bestankar

        misc=financial_balances.filter(title=FinancialBalanceTitleEnum.MISC).first()
        if misc is None:
            misc=FinancialBalance()
            misc.financial_document_id=self.pk
            misc.title=FinancialBalanceTitleEnum.MISC
            misc.save()

        misc.bestankar=self.bestankar-sum_bestankar
        misc.bedehkar=self.bedehkar-sum_bedehkar
        misc.save()
        if misc.bestankar==0 and misc.bedehkar==0:
            misc.delete()
    

    class Meta:
        verbose_name = _("FinancialDocument")
        verbose_name_plural = _("FinancialDocuments")

    def __str__(self):
        return f"""{self.account.title} : {self.transaction.title} : {self.transaction.amount}"""
    def normalize_balances(self,*args, **kwargs):
        balances=FinancialBalance.objects.filter(financial_document_id=self.pk)
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
    color_origin=models.ForeignKey("core.color", verbose_name=_("color"),null=True,blank=True, on_delete=models.SET_NULL)

    
    @property
    def color(self):
        if self.color_origin is None:
            # return Color(name="blue",code="#0000ff")
            color= getColor(self.title)
            return BS_ColorCode(color)
        else:
            return self.color_origin.code
     
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
    def bs_color(self):
        return getColor(self.title)


class FinancialDocumentTag(models.Model):
    title=models.CharField(_("title"), max_length=50)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'FinancialDocumentTag'
        verbose_name_plural = 'FinancialDocumentTags'


class Cheque(Transaction,LinkHelper):
    bank=models.ForeignKey("bank", verbose_name=_("bank"), on_delete=models.PROTECT)
    sayyad_no=models.CharField(_("شماره صیاد"), max_length=50)
    sarresid_datetime=models.DateTimeField(_("تاریخ سررسید"), auto_now=False, auto_now_add=False)
    serial_no=models.CharField(_("شماره سری و سریال چک"), max_length=50)
    @property
    def cheque_date(self):
        return self.sarresid_datetime
    
    def persian_cheque_date(self,no_tag=False):
        if no_tag:
            return PersianCalendar().from_gregorian(self.sarresid_datetime)
        return to_persian_datetime_tag(self.sarresid_datetime)
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
    tax_percent=models.IntegerField(_("درصد مالیات"),default=0)
    invoice_datetime=models.DateTimeField(_("تاریخ فاکتور"), auto_now=False, auto_now_add=False)
    ship_fee=models.IntegerField(_("هزینه حمل"),default=0)
    discount=models.IntegerField(_("تخفیف"),default=0)
 
    def get_official_print_url(self):
        return reverse(APP_NAME+":invoice_official_print",kwargs={'pk':self.pk})
    
    def get_letter_of_intent_url(self):
        return reverse(APP_NAME+":invoice_letter_of_intent",kwargs={'pk':self.pk})

    def get_print_url(self):
        return reverse(APP_NAME+":invoice_print_currency",kwargs={'pk':self.pk,'currency':'r'})
    def get_excel_url(self):
        return reverse(APP_NAME+":invoice_excel",kwargs={'pk':self.pk})
    
    def get_title(self):
        return self.title or f"فاکتور شماره {self.pk}"
  
    def get_edit_url2(self):
        return reverse(APP_NAME+":edit_invoice",kwargs={'pk':self.pk})
    def get_print_url_2(self):
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
    def calculate_sum(self):
        self.amount=self.sum_total()

    def save(self,*args, **kwargs):
        if self.description is None or self.description=="":
            self.description="این فاکتور فقط برای استعلام قیمت بوده و هیچ گونه ارزش قانونی دیگری ندارد."
        if self.class_name is None:
            self.class_name='invoice' 
        if self.app_name is None:
            self.app_name=APP_NAME
        if self.title is None or self.title=="":
            self.title=f"فاکتور شماره {self.pk}"
        self.calculate_sum()
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

    def normalize_rows(self):
        i=0
        for invoice_line in self.invoice_lines().order_by('row'):
            i+=1
            if not invoice_line.row-i==0:
                invoice_line.row=i
                invoice_line.save()


class InvoiceLine(models.Model,LinkHelper):
    date_added=models.DateTimeField(_("date_added"), auto_now=False, auto_now_add=True)
    invoice=models.ForeignKey("invoice",blank=True, verbose_name=_("invoice"),related_name="lines", on_delete=models.CASCADE)
    row=models.IntegerField(_("row"),default=1,blank=True)
    product_or_service=models.ForeignKey("productorservice", verbose_name=_("productorservice"), on_delete=models.CASCADE)
    quantity=models.FloatField(_("quantity"))
    discount=models.IntegerField(_("discount"),default=0)
    unit_price=models.IntegerField(_("unit_price"))
    unit_name=models.CharField(_("unit_name"),max_length=50,choices=UnitNameEnum.choices,default=UnitNameEnum.ADAD)
    description=models.CharField(_("description"),null=True,blank=True, max_length=50)
    class_name="invoiceline"
    app_name=APP_NAME 
    def save(self,*args, **kwargs):
        if not self.invoice.editable:
            return None
        super(InvoiceLine,self).save(*args, **kwargs)
        self.invoice.save()
        # for invoice_line in self.invoice.invoice_lines().order_by('row'):
        #     i+=1
        #     if not invoice_line.row-i==0:
        #         invoice_line.row=i
        #         invoice_line.save()
    def delete(self,*args, **kwargs):
        if not self.invoice.editable:
            return None
        invoice=self.invoice
        invoice=self.invoice
        super(InvoiceLine,self).delete()
        
        invoice.calculate_sum()
        invoice.save()
        invoice.normalize_rows()
        # i=0
        # for invoice_line in invoice.invoice_lines().order_by('row'):
        #     i+=1
        #     if not invoice_line.row-i==0:
        #         invoice_line.row=i
        #         invoice_line.save()

    class Meta:
        verbose_name = _("InvoiceLine")
        verbose_name_plural = _("InvoiceLines")

    def __str__(self):
        return f"{self.invoice} {self.row} - {self.product_or_service.title} "
    def line_total(self):
        return self.unit_price*self.quantity

    @property
    def product(self):
        return Product.objects.filter(pk=self.pk).first()

    @property
    def service(self):
        return Service.objects.filter(pk=self.pk).first()


class Category(models.Model,LinkHelper, ImageMixin):
    thumbnail_origin = models.ImageField(_("تصویر کوچک"), upload_to=IMAGE_FOLDER+'Category/Thumbnail/',null=True, blank=True, height_field=None, width_field=None, max_length=None)
    header_origin = models.ImageField(_("تصویر سربرگ"), upload_to=IMAGE_FOLDER+'Category/Header/',null=True, blank=True, height_field=None, width_field=None, max_length=None)
    parent=models.ForeignKey("category",blank=True,null=True, verbose_name=_("parent"),related_name="childs", on_delete=models.SET_NULL)
    title=models.CharField(_("title"), max_length=200)
    for_home=models.BooleanField(_("for_home"),default=False)
    priority=models.IntegerField(_("اولویت / ترتیب"),default="1000")
    products_or_services=models.ManyToManyField("accounting.productorservice", blank=True,verbose_name=_("products or services"))
    full_title=models.CharField(_("full_title"),null=True,blank=True, max_length=500)
    class_name='category'
    app_name=APP_NAME
    def save(self):
        self.full_title=self.full_title_
        super(Category,self).save()
    @property
    def products(self):
        ids=[]
        for products_or_service in self.products_or_services.all():
            ids.append(products_or_service.id)
        products=Product.objects.filter(id__in=ids)
        return products

    @property
    def services(self):
        ids=[]
        for products_or_service in self.products_or_services.all():
            ids.append(products_or_service.id)
        services=Service.objects.filter(id__in=ids)
        return services
    
    def __str__(self):
        return self.title
    
    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'
 
    def get_breadcrumb_link(self,*args, **kwargs):
        if "app_name" in kwargs:
            get_absolute_url=reverse(kwargs['app_name']+":category",kwargs={'pk':self.pk})
        else:
            get_absolute_url=self.get_absolute_url()
        aaa=""
        if self.parent is not None:
            aaa+="/"
        aaa+=f"""
                    <a href="{get_absolute_url}">
                    <span class="farsi">
                    {self.title}
                    </span>
                    </a> 
                    """
        if self.parent is None:
            return aaa
        return self.parent.get_breadcrumb_link(*args, **kwargs)+aaa
    
    def get_market_breadcrumb_link(self,*args, **kwargs):
        return self.get_breadcrumb_link(app_name="market")
    def get_market_breadcrumb_link1(self,*args, **kwargs):
        get_absolute_url=reverse("market:category",kwargs={'pk':self.pk})
        aaa=""
        if self.parent is not None:
            aaa+="/"
        aaa+=f"""
                    <a href="{get_absolute_url}">
                    <span class="farsi">
                    {self.title}
                    </span>
                    </a> 
                    """
        if self.parent is None:
            return aaa
        return self.parent.get_market_breadcrumb_link(*args, **kwargs)+aaa
     
    def get_breadcrumb_tag(self):
        return f"""
        
                
                    {self.get_breadcrumb_link()}
               
        """
    
    def get_market_breadcrumb_tag(self):
        return f"""
                    {self.get_market_breadcrumb_link()}
        """
    
    @property
    def full_title_(self):
        if self.parent is None:
            if self.title is None:
                return ""
            return self.title
        else:
            return self.parent.full_title_+" / " +self.title

    def get_market_absolute_url(self):
        return reverse("market:category",kwargs={'pk':self.pk})


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
            self.transaction_datetime=PersianCalendar().date
        super(Payment,self).save(*args, **kwargs)


class Salary(Spend,LinkHelper):    
    class_name="wage"
    month=models.IntegerField(_("month"))
    year=models.IntegerField(_("year"))
    def month_year(self):
        return PERSIAN_MONTH_NAMES[self.month]+" " + str(self.year)
    
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
    def cost_color(self):
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
        self.spend_type=SpendTypeEnum.COST
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
