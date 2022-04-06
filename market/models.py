from accounting.models import Invoice,Product as AccountingProduct
from core.models import _,LinkHelper,models,reverse
from market.apps import APP_NAME
# Create your models here.


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


class Category(models.Model,LinkHelper):
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