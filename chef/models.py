from django.db import models
from accounting.models import Invoice,Product as AccountingProduct
from django.utils.translation import gettext as _
from django.shortcuts import reverse
from chef.apps import APP_NAME
from chef.enums import MealTypeEnum
from core.models import Page
from utility.calendar import PersianCalendar
from utility.utils import LinkHelper
# Create your models here.

 

class Food(Page):

    class Meta:
        verbose_name = _("Food")
        verbose_name_plural = _("Food")
 
    def save(self,*args, **kwargs):
        if self.class_name is None or self.class_name=="":
            self.class_name="food"
        if self.app_name is None or self.app_name=="":
            self.app_name=APP_NAME
        return super(Food,self).save(*args, **kwargs)



class Guest(models.Model,LinkHelper):
    account=models.ForeignKey("accounting.account", verbose_name=_("account"), on_delete=models.CASCADE)
    app_name=APP_NAME
    class_name="guest"
    class Meta:
        verbose_name = _("Guest")
        verbose_name_plural = _("Guests")

    def __str__(self):
        return self.account.title
 

    def get_absolute_url(self):
        return reverse(APP_NAME+":"+self.class_name, kwargs={"pk": self.pk})


class Meal(models.Model,LinkHelper):
    title=models.CharField(_("title"), max_length=50)
    host=models.ForeignKey("host", verbose_name=_("host"), on_delete=models.CASCADE)
    foods=models.ManyToManyField("food", verbose_name=_("food"))
    date_served=models.DateField(_("date_served"), auto_now=False, auto_now_add=False)
    meal_type=models.CharField(_("meal type"),choices=MealTypeEnum.choices, max_length=50)
    max_reserve=models.IntegerField(_("max"),default=100)
    reserved=models.IntegerField(_("reserved"),default=1)
    app_name=APP_NAME
    class_name="meal"

    def served_count(self):
        a=self.reservedmeal_set.exclude(date_served=None)
        sum=0
        for ss in a:
            sum+=ss.quantity
        return sum
    def update_reserved(self, *args, **kwargs):
        if 'guest_id' not in kwargs:
            return 0
        guest_id=kwargs['guest_id']
        reservedmeal=self.reservedmeal_set.filter(guest_id=guest_id).first()
        if reservedmeal is not None:
            self.reserved=reservedmeal.quantity
        else:
            self.reserved=0
        return self.reserved

    class_name="meal"
    def reserves_count(self):
        a=self.reservedmeal_set.all()
        sum=0
        for ss in a:
            sum+=ss.quantity
        return sum
    class Meta:
        verbose_name = _("Meal")
        verbose_name_plural = _("Meals")

    def __str__(self):
        return f"{str(self.title)} # {self.meal_type} @ {self.persian_date_served()}"
 
    def persian_date_served(self):
        return PersianCalendar().from_gregorian(self.date_served)[:10]

 
class ReservedMeal(models.Model,LinkHelper):
    quantity=models.IntegerField(_("تعداد"),default=1)
    guest=models.ForeignKey("guest", verbose_name=_("guest"), on_delete=models.CASCADE)
    meal=models.ForeignKey("meal", verbose_name=_("meal"), on_delete=models.CASCADE)
    date_reserved=models.DateTimeField(_("date_reserved"), auto_now=False, auto_now_add=True)
    date_served=models.DateTimeField(_("date_served"),null=True,blank=True, auto_now=False, auto_now_add=False)
    class_name="reservedmeal"
    app_name=APP_NAME
    class Meta:
        verbose_name = _("ReservedMeal")
        verbose_name_plural = _("ReservedMeals")

    def persian_date_reserved(self):
        return PersianCalendar().from_gregorian(self.date_reserved)


    def __str__(self):
        return f"""{("***" if self.date_served is not None else "")} {str(self.guest)} {str(self.meal)}"""

    def get_absolute_url(self):
        return reverse(APP_NAME+":"+self.class_name, kwargs={"pk": self.pk})

    def get_edit_url(self):
        return f"{ADMIN_URL}{APP_NAME}/{self.class_name}/{self.pk}/change/"

        
    def persian_date_served(self):
        return PersianCalendar().from_gregorian(self.date_served)


class Host(models.Model,LinkHelper):
    title=models.CharField(_("title"), max_length=100)
    account=models.ForeignKey("accounting.account", verbose_name=_("account"), on_delete=models.CASCADE)
    class_name="host"
    app_name=APP_NAME
    class Meta:
        verbose_name = _("Host")
        verbose_name_plural = _("Hosts")

    def __str__(self):
        return self.title
  