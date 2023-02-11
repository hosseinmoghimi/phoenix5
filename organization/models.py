from django.db import models
from django.forms import CharField
from requests import request
from organization.apps import APP_NAME
from core.models import _,reverse,Page,LinkHelper
from utility.calendar import to_persian_datetime_tag
from organization.enums import *
class OrganizationUnit(Page):
    pre_title = models.CharField(
        _("pre_title"), blank=True, null=True, max_length=50)
    account = models.ForeignKey("accounting.account",verbose_name=_(
        "account"), on_delete=models.CASCADE)
    parent = models.ForeignKey("organizationunit", related_name="childs",
                               null=True, blank=True, verbose_name=_("parent"), on_delete=models.CASCADE)
    def all_childs_ids(self):
        pages_ids=[]
        for page in self.childs.all():
            chds= page.all_childs_ids()
            pages_ids.append(page.pk)
            for page1 in chds:
                pages_ids.append(page1)
        return pages_ids

    @property
    def root_title(self):
        if self.parent is None:
            return self.title
        return self.parent.root_title
    @property
    def employees(self,*args, **kwargs):
        return Employee.objects.filter(organization_unit_id=self.pk)
            
    @property
    def full_title(self,*args, **kwargs):
        a=""
        if self.parent is not None:
            a+=" "+self.parent.full_title
        return self.title+a
                                
    def all_sub_orgs(self):
        ids=self.all_childs_ids()
        ids.append(self.pk)
        return OrganizationUnit.objects.filter(id__in=ids)

    
    def __str__(self):
        # return self.title
        return self.full_title

    class Meta:
        verbose_name = _("OrganizationUnit")
        verbose_name_plural = _("واحد های سازمانی")

    def save(self, *args, **kwargs):
        if self.class_name is None or self.class_name == "":
            self.class_name = "organizationunit"
        if self.app_name is None or self.app_name == "":
            self.app_name = APP_NAME
        return super(OrganizationUnit, self).save(*args, **kwargs)
    def logo(self):
        if self.thumbnail_origin:
            return self.thumbnail
        elif self.parent is not None:
            return self.parent.thumbnail
        else:
            return self.thumbnail

    def get_chart_url(self):
        return reverse(APP_NAME+":org_chart",kwargs={'pk':self.pk})

class Employee(models.Model,LinkHelper):
    account=models.ForeignKey("accounting.account", verbose_name=_("account"), on_delete=models.CASCADE)
    organization_unit = models.ForeignKey("organizationunit", null=True, blank=True, verbose_name=_(
        "organization_unit"), on_delete=models.CASCADE)
    job_title = models.CharField(
        _("job title"), default="سرپرست", max_length=50)
    class_name = 'employee'
    app_name = APP_NAME
    @property
    def title(self):
        return self.account.title
    def get_salary_url(self):
        return reverse('salary:employee',kwargs={'pk':self.pk})

    @property
    def image(self):
        return self.account.logo


    def my_pages_ids(self):
        my_pages_ids=[]
        my_project_ids=self.my_project_ids()
        my_pages_ids=my_pages_ids+ my_project_ids
        return my_pages_ids

 
    @property
    def name(self):
        return self.account.title

    class Meta:
        verbose_name = _("Employee")
        verbose_name_plural = _("پرسنل و کارکنان")

    def __str__(self):
        return f"""{self.account.title} : {self.job_title} {str(self.organization_unit) if self.organization_unit is not None else ""} """

    def get_absolute_url(self):
        return reverse(APP_NAME+":employee", kwargs={"pk": self.pk})

    def my_project_ids(self):
        ids = []
        if self.organization_unit is not None:
            # for org in self.organization_unit_set.all():
            for proj in self.organization_unit.project_set.all():
                ids.append(proj.id)
            for proj in self.organization_unit.projects_employed.all():
                ids.append(proj.id)
            for proj in self.organization_unit.projects_contracted.all():
                ids.append(proj.id)
            # ids=(proj for proj in self.organization_unit.project_set.all())
        return ids

    def save(self, *args, **kwargs):
        return super(Employee, self).save(*args, **kwargs)



class LetterSent(models.Model,LinkHelper):
    sender = models.ForeignKey("organization.organizationunit", related_name="sent_letters", verbose_name=_(
        "فرستنده"), on_delete=models.CASCADE)
    recipient = models.ForeignKey("organization.organizationunit", related_name="inbox_letters", verbose_name=_(
        "گیرنده"), on_delete=models.CASCADE)
    letter = models.ForeignKey("letter", verbose_name=_(
        "letter"), on_delete=models.CASCADE)
    profile=models.ForeignKey("authentication.profile", verbose_name=_("profile"), on_delete=models.CASCADE)
    paraf=models.CharField(_("paraf"), max_length=500)
    description=models.CharField(_("paraf"), max_length=5000)
    date_sent = models.DateTimeField(
        _("date sent"), auto_now=False, auto_now_add=False)
    class_name="lettersent"
    app_name=APP_NAME
    
    class Meta:
        verbose_name = 'LetterSent'
        verbose_name_plural = 'سیر ارسال نامه ها'

    def persian_date_sent(self):
        return to_persian_datetime_tag(self.date_sent)


class Letter(Page):
    creator_organization_unit=models.ForeignKey("organizationunit", verbose_name=_("واحد ایجاد کننده"), on_delete=models.CASCADE)
    creator=models.ForeignKey("authentication.profile", verbose_name=_("ایجاد کننده"), on_delete=models.CASCADE)
    status=models.CharField(_("status"),choices=LetterStatusEnum.choices,default=LetterStatusEnum.DRAFT, max_length=50)
    def persian_date_added(self):
        return to_persian_datetime_tag(self.date_added)

    def save(self, *args, **kwargs):
        if self.class_name is None:
            self.class_name = "letter"
        if self.app_name is None:
            self.app_name = APP_NAME
        return super(Letter, self).save(*args, **kwargs)
    def get_print_url(self):
        return reverse(APP_NAME+":letter_print",kwargs={'pk':self.pk})
    class Meta:
        verbose_name = 'Letter'
        verbose_name_plural = 'نامه های اداری'

    def current_organization_unit(self):
        sents=LetterSent.objects.filter(letter_id=self.pk).order_by('date_sent')
        if len(sents)>0:
            return sents.last().recipient
        return self.creator_organization_unit