from django.utils import timezone
from utility.calendar import PersianCalendar
from django.db import models
from accounting.models import Invoice, InvoiceLine,Service
from core.enums import UnitNameEnum
from market.models import Product
from django.utils.translation import gettext as _
from django.shortcuts import reverse

from core.models import Page
from projectmanager.enums import *
from utility.utils import LinkHelper
from .apps import APP_NAME
# Create your models here.
from accounting.models import Account

class ProjectInvoice(Invoice):
    # project=models.ForeignKey("project", verbose_name=_("project"), on_delete=models.CASCADE)

    project_id=models.IntegerField(_("project_id"))
    @property
    def project(self):
        return Project.objects.filter(pk=self.project_id).first()
 

    class Meta:
        verbose_name = _("ProjectInvoice")
        verbose_name_plural = _("ProjectInvoices")
 


    def save(self,*args, **kwargs):
        project=self.project
        if project is not None and project.employer.account is not None and project.contractor.account is not None:
            self.pay_to_id=project.employer.account.id
            self.pay_from_id=project.contractor.account.id
            self.transaction_datetime=timezone.now()
            self.invoice_datetime=timezone.now()
        super(ProjectInvoice,self).save(*args, **kwargs)    
 
class MaterialInvoice(ProjectInvoice):

    

    class Meta:
        verbose_name = _("MaterialInvoice")
        verbose_name_plural = _("MaterialInvoices")
  

    def save(self,*args, **kwargs):
        self.class_name="materialinvoice"
        self.app_name=APP_NAME
        return super(MaterialInvoice,self).save(*args, **kwargs)


class ServiceInvoice(ProjectInvoice):

    

    class Meta:
        verbose_name = _("ServiceInvoice")
        verbose_name_plural = _("ServiceInvoices")
 


    def save(self,*args, **kwargs):
        self.class_name="serviceinvoice"
        self.app_name=APP_NAME
        return super(ServiceInvoice,self).save(*args, **kwargs)


class Request(models.Model):
    product_or_service=models.ForeignKey("accounting.productorservice", verbose_name=_("product or service"), on_delete=models.CASCADE)
    project=models.ForeignKey("project", verbose_name=_("project"), on_delete=models.CASCADE)
    quantity=models.FloatField(_("quantity"))
    unit_price=models.IntegerField(_("unit_price"))
    unit_name=models.CharField(_("unit_name"),choices=UnitNameEnum.choices,default=UnitNameEnum.ADAD, max_length=50)
    date_requested=models.DateTimeField(_("date_requested"), auto_now=False, auto_now_add=False)
    employee=models.ForeignKey("employee", verbose_name=_("employee"), on_delete=models.CASCADE)
    status=models.CharField(_("status"),choices=RequestStatusEnum.choices, max_length=50)
    @property
    def product(self):
        from market.models import Product
        return Product.objects.filter(pk=self.product_or_service_id).first()

    @property
    def service(self):
        from accounting.models import Service
        return Service.objects.filter(pk=self.product_or_service_id).first()

    class Meta:
        verbose_name = _("Request")
        verbose_name_plural = _("Requests")

    def save_invoice(self):
        invoice_line=InvoiceLine()
        invoice_line.product_or_service_id=self.product_or_service.id
        invoice_line.quantity=self.quantity
        invoice_line.unit_name=self.unit_name
        invoice_line.unit_price=self.unit_price
        if self.product is not None:
            invoice,res=MaterialInvoice.objects.get_or_create(project_id=self.project.pk)
        if self.service is not None:
            invoice,res=ServiceInvoice.objects.get_or_create(project_id=self.project.pk)
        invoice_line.invoice=invoice
        invoice_line.row=len(invoice.lines.all())+1
        invoice_line.save()

    def save(self,*args, **kwargs):
        print(100*"#")
        super(Request,self).save(*args, **kwargs)
        if self.project is not None and self.project.employer.account is not None and self.project.contractor.account is not None:
            self.save_invoice()
        else:
            return
        
            

    def __str__(self):
        return f"درخواست {self.quantity}  {self.unit_name} {self.product_or_service.title} برای پروژه {self.project} توسط {self.employee}"

    def get_absolute_url(self):
        return reverse("Request_detail", kwargs={"pk": self.pk})



class RequestSignature(models.Model,LinkHelper):
    request = models.ForeignKey("request", verbose_name=_(
        "request"), on_delete=models.CASCADE)
    employee = models.ForeignKey("employee", verbose_name=_(
        "employee"), on_delete=models.PROTECT)
    date_added = models.DateTimeField(
        _("date_added"), auto_now=False, auto_now_add=True)
    description = models.CharField(_("description"), max_length=200)
    status = models.CharField(_("status"), choices=SignatureStatusEnum.choices,
                              default=SignatureStatusEnum.REQUESTED, max_length=200)

    class_name = "requestsignature"
    app_name = APP_NAME

    class Meta:
        verbose_name = _("RequestSignature")
        verbose_name_plural = _("RequestSignatures")

    def persian_date_added(self):
        return PersianCalendar().from_gregorian(self.date_added)

    def get_status_color(self):
        return StatusColor(self.status)

    def get_status_tag(self):
        return f"""
            <span class="badge badge-{self.get_status_color()}">{self.status}</span>
        """

    def __str__(self):
        return f"""{self.request} : امضاءکننده" {self.employee}  " :{self.status} """

    def get_absolute_url(self):
        return reverse("RequestSignature_detail", kwargs={"pk": self.pk})
 


class Employee(Account):
    organization_unit=models.ForeignKey("organizationunit", verbose_name=_("organization_unit"), on_delete=models.CASCADE)
    job_title=models.CharField(_("job title"), max_length=50)

    class Meta:
        verbose_name = _("Employee")
        verbose_name_plural = _("Employees")

    def __str__(self):
        return f"{self.profile.name} : {self.job_title} {str(self.organization_unit)}"

    def get_absolute_url(self):
        return reverse("Employee_detail", kwargs={"pk": self.pk})


class OrganizationUnit(Page):
    account=models.ForeignKey("accounting.account",null=True,blank=True, verbose_name=_("account"), on_delete=models.CASCADE)
    parent=models.ForeignKey("OrganizationUnit",related_name="childs",null=True,blank=True, verbose_name=_("parent"), on_delete=models.CASCADE)
    def __str__(self):
        # return self.title
        return self.title+" "+(str(self.parent) if self.parent is not None and not self.parent.id==self.id else "")

    class Meta:
        verbose_name = _("OrganizationUnit")
        verbose_name_plural = _("OrganizationUnits")
    def save(self,*args, **kwargs):
        if self.class_name is None or self.class_name=="":
            self.class_name="organizationunit"
        if self.app_name is None or self.app_name=="":
            self.app_name=APP_NAME
        return super(OrganizationUnit,self).save(*args, **kwargs)
 
 
class Project(Page):
    employer=models.ForeignKey("organizationunit",related_name="projects_employed", verbose_name=_("کارفرما"), on_delete=models.CASCADE)    
    contractor=models.ForeignKey("organizationunit",related_name="projects_contracted", verbose_name=_("پیمانکار"), on_delete=models.CASCADE)    
    

    class Meta:
        verbose_name = _("Project")
        verbose_name_plural = _("Projects")
 
    def save(self,*args, **kwargs):
        if self.class_name is None or self.class_name=="":
            self.class_name='project'
        if self.app_name is None or self.app_name=="":
            self.app_name=APP_NAME
        super(Project,self).save(*args, **kwargs)

class SampleForm(Page):
    

    class Meta:
        verbose_name = _("SampleForm")
        verbose_name_plural = _("فرم های اداری نمونه")

    def save(self):
        if self.class_name is None or self.class_name=="":
            self.class_name="sampleform"
        if self.app_name is None or self.app_name=="":
            self.app_name=APP_NAME
        return super(SampleForm,self).save()
 