from accounting.models import Invoice,Product as AccountingProduct
from core.constants import CURRENCY
from core.enums import UnitNameEnum
from core.models import ImageMixin, _,LinkHelper,models,reverse,Page
from market.apps import APP_NAME
from accounting.models import Product
# Create your models here.
IMAGE_FOLDER = APP_NAME+"/images/"

class Brand(Page):


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


class Order(Invoice):
    

    class Meta:
        verbose_name = _("Order")
        verbose_name_plural = _("Orders")
 

    def get_absolute_url(self):
        return reverse("Order_detail", kwargs={"pk": self.pk})


    def save(self,*args, **kwargs):
        if self.class_name is None or self.class_name=="":
            self.class_name="order"
        if self.app_name is None or self.app_name=="":
            self.app_name=APP_NAME
        return super(Order,self).save(*args, **kwargs)
 
 
class Category(models.Model,LinkHelper, ImageMixin):
    thumbnail_origin = models.ImageField(_("تصویر کوچک"), upload_to=IMAGE_FOLDER+'Category/Thumbnail/',null=True, blank=True, height_field=None, width_field=None, max_length=None)
    parent=models.ForeignKey("category",blank=True,null=True, verbose_name=_("parent"),related_name="childs", on_delete=models.SET_NULL)
    title=models.CharField(_("title"), max_length=50)
    for_home=models.BooleanField(_("for_home"),default=False)
    products=models.ManyToManyField("accounting.product", blank=True,verbose_name=_("products"))
    class_name='category'
    app_name=APP_NAME
    def __str__(self):
        return self.title
    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'

    def get_products_list_url(self):
        return reverse(APP_NAME+":api_category_products",kwargs={'category_id':self.pk})
    def get_breadcrumb_tag_temp(self):
        breadcrumb_tag=""

        return breadcrumb_tag
    def get_breadcrumb_link(self):
        aaa=""
        if self.parent is not None:
            aaa+="/"
        aaa+=f"""
                    <a href="{self.get_absolute_url()}">
                    <span class="farsi">
                    {self.title}
                    </span>
                    </a> 
                    """
        if self.parent is None:
            return aaa
        return self.parent.get_breadcrumb_link()+aaa
    def get_breadcrumb_tag(self):
        return f"""
        
                
                    {self.get_breadcrumb_link()}
               
        """
       
class Supplier(Page):
    account=models.ForeignKey("accounting.account", verbose_name=_("account"), on_delete=models.CASCADE)
    

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


class Customer(models.Model,LinkHelper):
    account=models.ForeignKey("accounting.account", verbose_name=_("account"), on_delete=models.CASCADE)
    class_name="customer"
    app_name=APP_NAME

    class Meta:
        verbose_name = _("Customer")
        verbose_name_plural = _("Customers")

    def __str__(self):
        return self.title
 
    def save(self,*args, **kwargs):
        if self.class_name is None or self.class_name=="":
            self.class_name="customer"
        if self.app_name is None or self.app_name=="":
            self.app_name=APP_NAME
        return super(Customer,self).save(*args, **kwargs)



 
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

class Shop(models.Model,LinkHelper):
    supplier=models.ForeignKey("supplier", verbose_name=_("supplier"), on_delete=models.CASCADE)
    product_or_service=models.ForeignKey("accounting.productorservice", verbose_name=_("product_or_service"), on_delete=models.CASCADE)
    available=models.IntegerField(_("available"))
    unit_name=models.CharField(_("unit_name"),choices=UnitNameEnum.choices,default=UnitNameEnum.ADAD, max_length=50)
    unit_price=models.IntegerField(_("unit_price"))
    class_name="shop"
    app_name=APP_NAME
    @property
    def in_carts(self):
        counter=0
        for cart_line in CartLine.objects.filter(product_or_service=self.product_or_service):
            counter+=cart_line.quantity
        return counter
    

    class Meta:
        verbose_name = _("Shop")
        verbose_name_plural = _("Shops")

    def __str__(self):
        return f"{self.supplier.title} /{self.product_or_service.title} / هر {self.unit_name}:{self.unit_price} {CURRENCY}"
 

class CartLine(models.Model,LinkHelper):
    customer=models.ForeignKey("customer", verbose_name=_("customer"), on_delete=models.CASCADE)
    shop=models.ForeignKey("shop", verbose_name=_("shop"), on_delete=models.CASCADE)
    quantity=models.IntegerField(_("quantity"))
    class Meta:
        verbose_name = _("CartLine")
        verbose_name_plural = _("CartLines")
  
    def __str__(self):
        return f"{self.shop.supplier.title} /{self.shop.product_or_service.title} / {self.customer.title} / {self.quantity}"
 
