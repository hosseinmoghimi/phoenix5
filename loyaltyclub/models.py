from utility.num import to_tartib
from django.db import models
from django.utils.translation import gettext as _
from .apps import APP_NAME
from core.models import LinkHelper
# Create your models here.

class Coupon(models.Model,LinkHelper):
    title=models.CharField(_("title"), max_length=50)
    order=models.ForeignKey("order", verbose_name=_("order"), on_delete=models.CASCADE)
    amount=models.IntegerField(_("amount"))

    class_name="coupon"
    app_name=APP_NAME
    

    class Meta:
        verbose_name = _("Coupon")
        verbose_name_plural = _("Coupons")

    def __str__(self):
        return f"{self.order.customer} {self.amount}"

 

class Coef(models.Model,LinkHelper):
    number=models.IntegerField(_("number"))
    percentage=models.IntegerField(_("percentage"),default=3)

    class_name="coef"
    app_name=APP_NAME
    def tartib(self):
        return to_tartib(self.number)

    class Meta:
        verbose_name = _("Coef")
        verbose_name_plural = _("Coefs")

    def __str__(self):
        return f"{self.number} {self.percentage}"
 

class Order(models.Model,LinkHelper):
    supplier=models.ForeignKey("market.supplier", verbose_name=_("supplier"), on_delete=models.CASCADE)
    customer=models.ForeignKey("market.customer", verbose_name=_("customer"), on_delete=models.CASCADE)
    invoice=models.ForeignKey("accounting.invoice",related_name="order_set", verbose_name=_("invoice"),null=True,blank=True, on_delete=models.CASCADE)
    # title=models.CharField(_("title"), max_length=50)
    sum=models.IntegerField(_("sum"),default=0)
    ship_fee=models.IntegerField(_("هزینه حمل"),default=0)
    discount=models.IntegerField(_("تخفیف"),default=0)
    # paid=models.IntegerField(_("paid"))
    date_ordered=models.DateTimeField(_("date_ordered"), auto_now=False, auto_now_add=False)
    def save(self):
        super(Order,self).save()
    @property
    def paid(self):
        return self.sum-self.discount
    @property
    def title(self):
        orders=Order.objects.filter(date_ordered__lte=self.date_ordered).order_by("id")
        i=0
        ii=0
        for order in orders:
            i+=1
            if order.id==self.id:
                ii=i

        return f"سفارش شماره {ii}"
    def persian_date_ordered_tag(self):
        from utility.calendar import to_persian_datetime_tag
        return to_persian_datetime_tag(self.date_ordered)
    def persian_date_ordered(self):
        from utility.calendar import PersianCalendar
        return PersianCalendar().from_gregorian(self.date_ordered)
    app_name=APP_NAME
    class_name="order"

    class Meta:
        verbose_name = _("Order")
        verbose_name_plural = _("Orders")

    def __str__(self):
        return self.title
 
 

