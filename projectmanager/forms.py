from django import forms
from .apps import APP_NAME

class AddRemoteClientForm(forms.Form):
    project_id=forms.IntegerField(required=True) 
    name=forms.CharField(max_length=50, required=False)
    active_directory=forms.CharField(max_length=100, required=False)
    work_group=forms.CharField(max_length=50, required=False)
    url=forms.CharField(max_length=500, required=False)
    local_ip=forms.CharField(max_length=50, required=False)
    remote_ip=forms.CharField(max_length=50, required=False)
    any_desk_address=forms.CharField(max_length=50, required=False)
    any_desk_password=forms.CharField(max_length=50, required=False)
    username=forms.CharField(max_length=50, required=False)
    password=forms.CharField(max_length=50, required=False)
    identity=forms.CharField(max_length=50, required=False)
    ssid=forms.CharField(max_length=50, required=False)
    preshared_key=forms.CharField(max_length=50, required=False)
    frequency=forms.CharField(max_length=50, required=False)
    protocol=forms.CharField(max_length=50, required=False)
    channel_width=forms.CharField(max_length=50, required=False)
    adsl_username=forms.CharField(max_length=50, required=False)
    adsl_password=forms.CharField(max_length=50, required=False)
    telephone=forms.CharField(max_length=50, required=False)
    contact=forms.CharField(max_length=50, required=False)
    description=forms.CharField(max_length=2000, required=False)

class CopyServiceRequestsForm(forms.Form):
    source_project_id=forms.IntegerField(required=True)
    destination_project_id=forms.IntegerField(required=True)
    invoice_id=forms.IntegerField(required=True)
    status=forms.CharField(max_length=50, required=False)
    
class CopyMaterialRequestsForm(forms.Form):
    source_project_id=forms.IntegerField(required=True)
    destination_project_id=forms.IntegerField(required=True)
    invoice_id=forms.IntegerField(required=True)
    status=forms.CharField(max_length=50, required=False)



class CopyServiceRequestsFromInvoiceForm(forms.Form):
    source_invoice_id=forms.IntegerField(required=True)
    destination_project_id=forms.IntegerField(required=True)
    invoice_id=forms.IntegerField(required=True)
    status=forms.CharField(max_length=50, required=False)
    
class CopyMaterialRequestsFromInvoiceForm(forms.Form):
    source_invoice_id=forms.IntegerField(required=True)
    destination_project_id=forms.IntegerField(required=True)
    invoice_id=forms.IntegerField(required=True)
    status=forms.CharField(max_length=50, required=False)


class CopyProjectForm(forms.Form):
    project_id=forms.IntegerField(required=True)
 
class AddProjectForm(forms.Form):
    parent_id=forms.IntegerField(required=False)
    title=forms.CharField(max_length=50, required=True)
    contractor_id=forms.IntegerField(required=False)
    employer_id=forms.IntegerField(required=False)
    percentage_completed=forms.IntegerField(required=False)
    start_date=forms.CharField(max_length=50, required=False)
    end_date=forms.CharField(max_length=50, required=False)
    status=forms.CharField(max_length=50, required=False)
    


class AddMaterialRequestToWareHouseSheetForm(forms.Form):
    material_request_id=forms.IntegerField(required=True)
    ware_house_import_sheet_id=forms.IntegerField(required=False)
    ware_house_export_sheet_id=forms.IntegerField(required=False)
    ware_house_id=forms.IntegerField(required=False)
    employee_id=forms.IntegerField(required=False)
    date_exported=forms.CharField(max_length=50,required=False)
    serial_no=forms.CharField(max_length=50,required=False)
    description=forms.CharField(max_length=5000,required=False)
    


class AddEventForm(forms.Form):
    project_id=forms.IntegerField(required=True)
    event_datetime=forms.CharField( max_length=20, required=False)
    start_datetime=forms.CharField( max_length=20, required=False)
    end_datetime=forms.CharField( max_length=20, required=False)
    title=forms.CharField(max_length=500, required=True)


class AddMaterialRequestForm(forms.Form):
    invoice_id=forms.IntegerField(required=False)
    project_id=forms.IntegerField(required=True)
    quantity=forms.FloatField(required=True)
    employee_id=forms.IntegerField(required=False)
    material_id=forms.IntegerField(required=True)
    unit_price=forms.IntegerField(required=True)
    unit_name=forms.CharField(max_length=50, required=True)
    description=forms.CharField(max_length=500, required=False)

class EditProjectForm(forms.Form):
    title=forms.CharField(max_length=100, required=False)
    project_id=forms.IntegerField(required=True)
    weight=forms.IntegerField(required=False)
    percentage_completed=forms.IntegerField(required=True)
    employer_id=forms.IntegerField(required=False)
    contractor_id=forms.IntegerField(required=False)
    start_date=forms.CharField(max_length=20, required=True)
    end_date=forms.CharField(max_length=20, required=True)
    status=forms.CharField(max_length=50, required=False)
    archive=forms.BooleanField(required=False)

class CopyProjectRequestForm(forms.Form):
    source_project_id=forms.IntegerField(required=True)
    request_type=forms.CharField(max_length=50,required=True)

class AddSignatureForm(forms.Form):
    service_request_id=forms.IntegerField(required=False)
    material_request_id=forms.IntegerField(required=False)
    request_id=forms.IntegerField(required=True)
    description=forms.CharField(max_length=500,required=False)
    status=forms.CharField(max_length=50,required=True)


class AddEmployeeForm(forms.Form):
    organization_unit_id=forms.IntegerField(required=True)
    profile_id=forms.IntegerField(required=False)
    username=forms.CharField(max_length=50,required=False)
    password=forms.CharField(max_length=50,required=False)
    first_name=forms.CharField(max_length=50,required=False)
    last_name=forms.CharField(max_length=50,required=False)
               
class SearchForm(forms.Form): 
    url=("/"+APP_NAME+"/search/")
    search_for=forms.CharField(max_length=50, required=True)
          
class AddMaterialForm(forms.Form):
    title=forms.CharField(max_length=500, required=True)
    parent_id=forms.IntegerField( required=False)
          
class AddServiceForm(forms.Form):
    title=forms.CharField(max_length=500, required=True)
    parent_id=forms.IntegerField( required=False)
         
class AddServiceRequestForm(forms.Form):
    invoice_id=forms.IntegerField(required=False)
    project_id=forms.IntegerField(required=True)
    employee_id=forms.IntegerField(required=False)
    quantity=forms.FloatField(required=True)
    unit_price=forms.IntegerField(required=True)
    service_id=forms.IntegerField(required=False)
    unit_name=forms.CharField(max_length=50, required=True)
    service_title=forms.CharField(max_length=150, required=False)
    description=forms.CharField(max_length=500, required=False)
                     