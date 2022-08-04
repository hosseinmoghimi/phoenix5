from django.utils import timezone
from utility.calendar import PersianCalendar, to_persian_datetime_tag
from django.db import models
from accounting.models import Invoice, InvoiceLine
from django.utils.translation import gettext as _
from django.shortcuts import reverse
from core.models import Page
from projectmanager.enums import *
from accounting.models import Product as Material, Service
from utility.utils import LinkHelper
from .apps import APP_NAME
# Create your models here.
from accounting.models import Account
from organization.models import OrganizationUnit,Employee,Letter,LetterSent
IMAGE_FOLDER = APP_NAME+"/images/"
from utility.currency import to_price

class ProjectInvoice(Invoice):
    # project=models.ForeignKey("project", verbose_name=_("project"), on_delete=models.CASCADE)

    project_id = models.IntegerField(_("project_id"))

    @property
    def project(self):
        return Project.objects.filter(pk=self.project_id).first()

    class Meta:
        verbose_name = _("ProjectInvoice")
        verbose_name_plural = _("ProjectInvoices")

    def save(self, *args, **kwargs):
        project = self.project
        if project is not None and project.employer.account is not None and project.contractor.account is not None:
            self.pay_to_id = project.employer.account.id
            self.pay_from_id = project.contractor.account.id
            self.transaction_datetime = PersianCalendar().date
            self.invoice_datetime = PersianCalendar().date
        super(ProjectInvoice, self).save(*args, **kwargs)


class MaterialInvoice(ProjectInvoice):

    class Meta:
        verbose_name = _("MaterialInvoice")
        verbose_name_plural = _("MaterialInvoices")

    def save(self, *args, **kwargs):
        if self.title is None or self.title == "":
            self.title = "فاکتور درخواست متریال  "+self.project.full_title
        self.class_name = "materialinvoice"
        self.app_name = APP_NAME

        return super(MaterialInvoice, self).save(*args, **kwargs)


class ServiceInvoice(ProjectInvoice):

    class Meta:
        verbose_name = _("ServiceInvoice")
        verbose_name_plural = _("ServiceInvoices")

    def save(self, *args, **kwargs):
        if self.title is None or self.title == "":
            self.title = "فاکتور درخواست سرویس  "+self.project.full_title
        self.class_name = "serviceinvoice"
        self.app_name = APP_NAME
        return super(ServiceInvoice, self).save(*args, **kwargs)
 

class Request(InvoiceLine, LinkHelper):
    project = models.ForeignKey("project", verbose_name=_(
        "project"), on_delete=models.CASCADE)
    date_delivered = models.DateTimeField(
        _("date_delivered"), auto_now=False, null=True, blank=True, auto_now_add=False)
    date_requested = models.DateTimeField(
        _("date_requested"), auto_now=False, null=True, blank=True, auto_now_add=False)
    employee = models.ForeignKey("organization.employee", verbose_name=_(
        "organization.employee"), on_delete=models.CASCADE)
    status = models.CharField(
        _("status"), choices=RequestStatusEnum.choices, max_length=50)
    type = models.CharField(_("type"), choices=RequestTypeEnum.choices,
                            default=RequestTypeEnum.MATERIAL_REQUEST, max_length=50)
    class_name = "request"
    app_name = APP_NAME

    @property
    def title(self):
        return f"درخواست {self.quantity}  {self.unit_name} {self.product_or_service.title} برای پروژه {self.project} "

    @property
    def product(self):
        # from market.models import Product
        return Material.objects.filter(pk=self.product_or_service_id).first()

    @property
    def material(self):
        return self.product
 
    @property
    def service(self):
        from accounting.models import Service
        return Service.objects.filter(pk=self.product_or_service_id).first()

    def get_status_tag(self):
        return f"""<span class="badge badge-pill badge-{self.get_status_color()}">{self.status}</span>"""

    class Meta:
        verbose_name = _("Request")
        verbose_name_plural = _("Requests")

    def save(self, *args, **kwargs):
        
        self.row = len(self.invoice.lines.all())+1
        super(Request, self).save(*args, **kwargs)

    def total(self):
        total = 0
        total = self.unit_price*self.quantity
        return total

    def persian_date_added(self):
        return PersianCalendar().from_gregorian(self.date_added)

    def persian_date_delivered(self):
        return PersianCalendar().from_gregorian(self.date_delivered)

    def persian_date_requested(self):
        return PersianCalendar().from_gregorian(self.date_requested)

    def can_be_edited(self):
        return self.project.can_be_edited

    def get_status_color(self):
        return StatusColor(self.status)

    def signatures(self):
        return RequestSignature.objects.filter(materialrequest=self).order_by('-date_added')

    def line_total(self):
        return self.quantity*self.unit_price

    def __str__(self):
        return f"درخواست {self.quantity}  {self.unit_name} {self.product_or_service.title} برای پروژه {self.project} توسط {self.employee}"

    def get_absolute_url(self):
        if self.product is not None:
            return reverse(APP_NAME+":materialrequest", kwargs={"pk": self.pk})

        if self.service is not None:
            return reverse(APP_NAME+":servicerequest", kwargs={"pk": self.pk})


class MaterialRequest(Request, LinkHelper):
    class Meta:
        verbose_name = 'MaterialRequest'
        verbose_name_plural = 'درخواست های متریال'

    def save(self, *args, **kwargs):
        self.class_name = "materialrequest"
        self.app_name = APP_NAME
        self.type = RequestTypeEnum.MATERIAL_REQUEST
        return super(MaterialRequest, self).save(*args, **kwargs)

 
class ServiceRequest(Request, LinkHelper):
    class Meta:
        verbose_name = 'ServiceRequest'
        verbose_name_plural = 'درخواست های سرویس'

    def save(self, *args, **kwargs):
        self.class_name = "servicerequest"
        self.type = RequestTypeEnum.SERVICE_REQUEST
        self.app_name = APP_NAME
        return super(ServiceRequest, self).save(*args, **kwargs)


class RequestSignature(models.Model, LinkHelper):
    request = models.ForeignKey("request", verbose_name=_(
        "request"), on_delete=models.CASCADE)
    employee = models.ForeignKey("organization.employee", verbose_name=_(
        "organization.employee"), on_delete=models.PROTECT)
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


class WareHouse(OrganizationUnit):

    def save(self, *args, **kwargs):
        if self.class_name is None:
            self.class_name = "warehouse"
        if self.app_name is None:
            self.app_name = APP_NAME
        return super(WareHouse, self).save(*args, **kwargs)

    class Meta:
        verbose_name = 'WareHouse'
        verbose_name_plural = 'WareHouses'



class Project(Page):
    parent = models.ForeignKey("project", verbose_name=_(
        "parent"),related_name="childs", null=True, blank=True, on_delete=models.CASCADE)
    status = models.CharField(_("status"), choices=ProjectStatusEnum.choices,
                              default=ProjectStatusEnum.DRAFT, max_length=50)
    employer = models.ForeignKey("organization.organizationunit", related_name="projects_employed", verbose_name=_(
        "کارفرما"), on_delete=models.CASCADE)
    contractor = models.ForeignKey("organization.organizationunit", related_name="projects_contracted", verbose_name=_(
        "پیمانکار"), on_delete=models.CASCADE)
    percentage_completed = models.IntegerField(
        _("درصد تکمیل پروژه"), default=0)
    start_date = models.DateTimeField(
        _("زمان شروع پروژه"), null=True, blank=True, auto_now=False, auto_now_add=False)
    end_date = models.DateTimeField(
        _("زمان پایان پروژه"), null=True, blank=True, auto_now=False, auto_now_add=False)
    organization_units = models.ManyToManyField(
        "organization.organizationunit", verbose_name=_("واحد های سازمانی"), blank=True)
    weight = models.IntegerField(_("ضریب و وزن پروژه"), default=10)
    color=models.CharField(_("color"),choices=ColorEnum.choices,default=ColorEnum.PRIMARY, max_length=50)
    # locations = models.ManyToManyField("map.location", blank=True, verbose_name=_("locations"))
    def all_childs_ids(self):
        pages_ids=[]
        for page in self.childs.all():
            chds= page.all_childs_ids()
            pages_ids.append(page.pk)
            for page1 in chds:
                pages_ids.append(page1)
        return pages_ids
    
    def all_sub_projects(self):
        return Project.objects.filter(id__in=self.all_childs_ids())


    def material_requests(self):
        return Request.objects.filter(project=self).filter(type=RequestTypeEnum.MATERIAL_REQUEST)

    @property
    def materialinvoice_set(self):
        return MaterialInvoice.objects.filter(project_id=self.pk)

    def service_requests(self):
        return Request.objects.filter(project=self).filter(type=RequestTypeEnum.SERVICE_REQUEST)

    def employees(self):
        employees = []
        for org in self.organization_units.all():
            for emp in org.employee_set.all():
                employees.append(emp.id)
        return Employee.objects.filter(id__in=employees)

    class Meta:
        verbose_name = _("Project")
        verbose_name_plural = _("Projects")

    # @property
    # def locations(self):
    #     from map.models import Location,PageLocation
    #     page_locations=PageLocation.objects.filter(page_id=self.pk)
    #     locations_id=list(page_locations.values('location_id'))
    #     ids=[]
    #     for location_id in locations_id:
    #         ids.append(location_id['location_id'])
    #     locations=Location.objects.filter(id__in=ids)
    #     return locations

    def persian_start_date(self):
        return PersianCalendar().from_gregorian(self.start_date)

    def persian_end_date(self):
        return PersianCalendar().from_gregorian(self.end_date)

    def auto_percentage_completed(self):
        sub_projects = self.sub_projects()
        if len(sub_projects) == 0:
            return self.percentage_completed
        auto_percentage_completed = 0
        sum_weight = 0
        for sub_project in sub_projects:
            auto_percentage_completed += sub_project.weight * \
                (sub_project.auto_percentage_completed())
            sum_weight += sub_project.weight
        auto_percentage_completed = auto_percentage_completed/sum_weight

        return round(auto_percentage_completed, 2)

    def update_accounting_data(self, *args, **kwargs):

        if self.status == ProjectStatusEnum.DRAFT:
            return
        if self.employer is None or self.employer.owner is None:
            return
        if self.contractor is None or self.contractor.owner is None:
            return

        from accounting.models import ProjectTransaction, FinancialAccount
        ProjectTransaction.objects.filter(project=self).delete()
        if (self.sum_material_requests()+self.sum_service_requests()) == 0:
            return
        pt = ProjectTransaction()
        pt.project = self
        pt.amount = self.sum_material_requests()+self.sum_service_requests()
        pt.pay_from = FinancialAccount.get_by_profile_or_new(
            profile_id=self.contractor.owner.id)
        pt.pay_to = FinancialAccount.get_by_profile_or_new(
            profile_id=self.employer.owner.id)
        pt.date_paid = self.date_added
        pt.title = f"""بابت حساب پروژه """
        pt.save()

    def get_status_color(self):
        return StatusColor(self.status)

    @property
    def full_title(self):
        if self.parent is None:
            return self.title
        return self.parent.full_title+" : "+self.title

    def sum_weight(self):
        sum_weight = 0
        sub_projects = self.sub_projects()
        if len(sub_projects) == 0:
            return 0
        for sub_project in sub_projects:
            sum_weight += sub_project.weight
        return sum_weight

    def save(self, *args, **kwargs):
        if self.class_name is None or self.class_name == "":
            self.class_name = 'project'
        if self.app_name is None or self.app_name == "":
            self.app_name = APP_NAME
        super(Project, self).save(*args, **kwargs)

    def sum_total(self):
        sum = 0
        for ii in self.invoices():
            sum += ii.sum_total()
        for child in self.childs.all():
            if not child.status==ProjectStatusEnum.DRAFT:
                sum+=child.sum_total()
        return sum

    def invoices(self):
        return ProjectInvoice.objects.filter(project_id=self.pk)

    def get_guantt_chart_url(self):
        return reverse(APP_NAME+":project_guantt",kwargs={'pk':self.pk})

    def get_sub_chart_url(self):
        return reverse(APP_NAME+":project_chart",kwargs={'pk':self.pk})
    def get_full_description_for_chart(self):
        return f"""
        <div><small class="text-muted">{to_price(self.sum_total())}</small></div>
        <div>{self.percentage_completed} %</div>
        """

class SampleForm(Page):

    class Meta:
        verbose_name = _("SampleForm")
        verbose_name_plural = _("فرم های اداری نمونه")

    def save(self):
        if self.class_name is None or self.class_name == "":
            self.class_name = "sampleform"
        if self.app_name is None or self.app_name == "":
            self.app_name = APP_NAME
        return super(SampleForm, self).save()


class Event(Page):
    project_related = models.ForeignKey(
        "project", verbose_name=_("project"), on_delete=models.CASCADE)
    event_datetime = models.DateTimeField(
        _("event_datetime"), auto_now=False, auto_now_add=False)
    start_datetime = models.DateTimeField(
        _("start_datetime"), auto_now=False, auto_now_add=False)
    end_datetime = models.DateTimeField(
        _("end_datetime"), auto_now=False, auto_now_add=False)
    # adder=models.ForeignKey("authentication.profile", verbose_name=_("profile"), on_delete=models.CASCADE)

    def save(self, *args, **kwargs):
        if self.app_name is None:
            self.app_name = APP_NAME
        if self.class_name is None:
            self.class_name = "event"
        return super(Event, self).save(*args, **kwargs)

    def persian_event_datetime(self):
        return PersianCalendar().from_gregorian(self.event_datetime)

    def persian_start_datetime(self):
        return PersianCalendar().from_gregorian(self.start_datetime)

    def persian_end_datetime(self):
        return PersianCalendar().from_gregorian(self.end_datetime)

    def start_datetime2(self):
        return self.start_datetime.strftime("%Y-%m-%d %H:%M")

    def end_datetime2(self):
        return self.end_datetime.strftime("%Y-%m-%d %H:%M")

    class Meta:
        verbose_name = _("Event")
        verbose_name_plural = _("رویداد ها")

 
 