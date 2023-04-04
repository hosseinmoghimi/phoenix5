from accounting.models import Invoice, InvoiceLine,Product as AccountingProduct
from core.constants import CURRENCY
from core.enums import UnitNameEnum
from market.enums import *
from django.utils import timezone
from core.models import ImageMixin, _,LinkHelper,models,reverse,Page
from market.apps import APP_NAME
from accounting.models import Product,Category
# Create your models here.
IMAGE_FOLDER = APP_NAME+"/images/"


class Brand(Page):
    products=models.ManyToManyField("accounting.product", blank=True,verbose_name=_("products"))

    @property
    def logo(self):
        return self.thumbnail
        
    class Meta:
        verbose_name = _("Brand")
        verbose_name_plural = _("Brands")

    def save(self,*args, **kwargs):
        if self.class_name is None or self.class_name=="":
            self.class_name='brand'
        if self.app_name is None or self.app_name=="":
            self.app_name=APP_NAME
        return super(Brand,self).save(*args, **kwargs)


class Order(Invoice,LinkHelper):
    class_name="order"
    app_name=APP_NAME

    class Meta:
        verbose_name = _("Order")
        verbose_name_plural = _("Orders")
 
    def save(self,*args, **kwargs):
        if self.class_name is None or self.class_name=="":
            self.class_name="order"
        if self.app_name is None or self.app_name=="":
            self.app_name=APP_NAME
        return super(Order,self).save(*args, **kwargs)
 
  
class Supplier(Page):
    region=models.ForeignKey("map.area", verbose_name=_("region"), on_delete=models.CASCADE)
    account=models.ForeignKey("accounting.account", verbose_name=_("account"), on_delete=models.CASCADE)
    
    def get_loyaltyclub_absolute_url(self):
        return reverse('loyaltyclub:supplier',kwargs={'pk':self.pk})

    class Meta:
        verbose_name = _("Supplier")
        verbose_name_plural = _("Suppliers")

    def __str__(self):
        return self.title
 
    def save(self,*args, **kwargs):
        if self.class_name is None or self.class_name=="":
            self.class_name="supplier"
        if self.app_name is None or self.app_name=="":
            self.app_name=APP_NAME
        return super(Supplier,self).save(*args, **kwargs)
    def get_loyaltyclub_absolute_url(self):
        return reverse("loyaltyclub:supplier",kwargs={'pk':self.pk})


class Customer(models.Model,LinkHelper):
    inviter=models.ForeignKey("customer", verbose_name=_("inviter"),null=True,blank=True, on_delete=models.SET_NULL)
    region=models.ForeignKey("map.area", verbose_name=_("region"), on_delete=models.CASCADE)
    level=models.CharField(_("level"),choices=CustomerLevelEnum.choices,default=CustomerLevelEnum.REGULAR, max_length=50)
    account=models.ForeignKey("accounting.account", verbose_name=_("account"), on_delete=models.CASCADE)
    class_name="customer"
    app_name=APP_NAME
    def get_loyaltyclub_absolute_url(self):
        return reverse('loyaltyclub:customer',kwargs={'pk':self.pk})
    class Meta:
        verbose_name = _("Customer")
        verbose_name_plural = _("Customers")

    def __str__(self):
        return self.account.title
 
    def save(self,*args, **kwargs):
        if self.class_name is None or self.class_name=="":
            self.class_name="customer"
        if self.app_name is None or self.app_name=="":
            self.app_name=APP_NAME
        return super(Customer,self).save(*args, **kwargs)


class MarketInvoice(Invoice):

    

    class Meta:
        verbose_name = _("MarketInvoice")
        verbose_name_plural = _("MarketInvoices")
 
    def save(self, *args, **kwargs):
        if self.title is None or self.title == "":
            self.title = "فاکتور فروش"
        self.class_name = "marketinvoice"
        self.app_name = APP_NAME

        return super(MarketInvoice, self).save(*args, **kwargs)

 
class Cart(Invoice):

    class Meta:
        verbose_name = _("Cart")
        verbose_name_plural = _("Carts")
 

    def save(self,*args, **kwargs):
        if self.class_name is None or self.class_name=="":
            self.class_name="cart"
        if self.app_name is None or self.app_name=="":
            self.app_name=APP_NAME
        return super(Cart,self).save(*args, **kwargs)


class CartLine(models.Model,LinkHelper):
    date_added=models.DateTimeField(_("date_added"), auto_now=False, auto_now_add=True)
    customer=models.ForeignKey("customer",blank=True, verbose_name=_("مشتری"), on_delete=models.CASCADE)
    row=models.IntegerField(_("row"),default=1,blank=True)
    quantity=models.FloatField(_("تعداد"))
    discount=models.IntegerField(_("تخفیف"),default=0)
    shop=models.ForeignKey("shop", verbose_name=_("shop"), on_delete=models.CASCADE)
    description=models.CharField(_("توضیحات"),null=True,blank=True, max_length=50)
    class_name="cartline"
    app_name=APP_NAME
    class Meta:
        verbose_name = _("CartLine")
        verbose_name_plural = _("CartLines")

    def __str__(self):
        return f"{self.customer} ^ {self.quantity} {self.shop.unit_name} * {self.shop.product_or_service.title} "
    def save(self,*args, **kwargs):
        old_ones=CartLine.objects.filter(customer_id=self.customer_id).filter(shop_id=self.shop_id)
        old_ones.delete()
        if len(old_ones)>0:
            old_ones.exclude(pk=old_ones.first().id).delete()
        super(CartLine,self).save()


class Shop(models.Model,LinkHelper):
    # region=models.ForeignKey("map.area", verbose_name=_("region"), on_delete=models.CASCADE)
    supplier=models.ForeignKey("supplier", verbose_name=_("supplier"), on_delete=models.CASCADE)
    product_or_service=models.ForeignKey("accounting.productorservice", verbose_name=_("product_or_service"), on_delete=models.CASCADE)
    available=models.IntegerField(_("available"))
    expire_datetime=models.DateTimeField(_("تاریخ اعتبار تا"), auto_now=False, auto_now_add=False)
    specifications=models.ManyToManyField("accounting.ProductSpecification",blank=True, verbose_name=_("ویژگی ها"))
    level=models.CharField(_("level"),choices=CustomerLevelEnum.choices,default=CustomerLevelEnum.REGULAR, max_length=50)
    unit_name=models.CharField(_("unit_name"),choices=UnitNameEnum.choices,default=UnitNameEnum.ADAD, max_length=50)
    old_price=models.IntegerField(_("old_price"))
    buy_price=models.IntegerField(_("buy_price"))
    unit_price=models.IntegerField(_("unit_price"))

    class_name="shop"
    app_name=APP_NAME

    @property
    def product(self):
        return Product.objects.filter(pk=self.product_or_service.pk).first()
        
    @property
    def in_carts(self):
        counter=0
        for cart_line in CartLine.objects.filter(shop__product_or_service=self.product_or_service):
            counter+=cart_line.quantity
        return counter
    
    def save(self, *args, **kwargs):
        if self.expire_datetime is None:
            self.expire_datetime =timezone.now()

        # if self.region is None:
        #     self.region=self.supplier.region

        return super(Shop, self).save(*args, **kwargs)

    class Meta:
        verbose_name = _("Shop")
        verbose_name_plural = _("Shops")

    def __str__(self):
        return f"{self.supplier.title} /{self.product_or_service.title} / هر {self.unit_name}:{self.unit_price} {CURRENCY}"
 

 