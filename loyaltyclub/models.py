from django.db import models
from django.utils.translation import gettext as _
from .apps import APP_NAME
from core.models import LinkHelper
# Create your models here.


class Order(models.Model,LinkHelper):
    supplier=models.ForeignKey("market.supplier", verbose_name=_("supplier"), on_delete=models.CASCADE)
    customer=models.ForeignKey("market.customer", verbose_name=_("customer"), on_delete=models.CASCADE)
    invoice=models.ForeignKey("accounting.invoice",related_name="order_set", verbose_name=_("invoice"),null=True,blank=True, on_delete=models.CASCADE)
    title=models.CharField(_("title"), max_length=50)
    sum=models.IntegerField(_("sum"),default=0)
    ship_fee=models.IntegerField(_("هزینه حمل"),default=0)
    discount=models.IntegerField(_("تخفیف"),default=0)
    coupon=models.IntegerField(_("تخفیف"),default=0)

    date_ordered=models.DateTimeField(_("date_ordered"), auto_now=False, auto_now_add=False)
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
 