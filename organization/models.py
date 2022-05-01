from django.db import models
from organization.apps import APP_NAME
from core.models import _,reverse,Page,LinkHelper


class OrganizationUnit(Page):
    pre_title = models.CharField(
        _("pre_title"), blank=True, null=True, max_length=50)
    account = models.ForeignKey("accounting.account", null=True, blank=True, verbose_name=_(
        "account"), on_delete=models.CASCADE)
    parent = models.ForeignKey("organizationunit", related_name="childs",
                               null=True, blank=True, verbose_name=_("parent"), on_delete=models.CASCADE)

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


    def my_pages_ids(self):
        my_pages_ids=[]
        my_project_ids=self.my_project_ids()
        my_pages_ids=my_pages_ids+ my_project_ids
        return my_pages_ids

    @property
    def mobile(self):
        return self.account.profile.mobile

    @property
    def name(self):
        return self.account.profile.name

    class Meta:
        verbose_name = _("Employee")
        verbose_name_plural = _("Employees")

    def __str__(self):
        return f"""{self.account.profile.name} : {self.job_title} {str(self.organization_unit) if self.organization_unit is not None else ""} """

    def get_absolute_url(self):
        return reverse(APP_NAME+":employee", kwargs={"pk": self.pk})

    def my_project_ids(self):
        ids = []
        if self.organization_unit is not None:
            # for org in self.organization_unit_set.all():
            for proj in self.organization_unit.project_set.all():
                ids.append(proj.id)
            # ids=(proj for proj in self.organization_unit.project_set.all())
        return ids

    def save(self, *args, **kwargs):
        return super(Employee, self).save(*args, **kwargs)

