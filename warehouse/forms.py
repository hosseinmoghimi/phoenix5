from django import forms

class AddWarehouseForm(forms.Form):
    title=forms.CharField(max_length=100, required=True)
     
class ChangeWarehouseSheetStateForm(forms.Form):
    warehouse_sheet_id=forms.IntegerField(required=True)
    status=forms.CharField(max_length=50, required=True)
    
class ReportForm(forms.Form):
    ware_house_sheet_id=forms.IntegerField(required=False)
    ware_house_id=forms.IntegerField(required=False)
    product_id=forms.IntegerField(required=False)
    status=forms.CharField(max_length=50, required=False)
     
class AddSignatureForm(forms.Form):
    ware_house_sheet_id=forms.IntegerField(required=False)
    employee_id=forms.IntegerField(required=False)
    description=forms.CharField(max_length=50, required=False)
    status=forms.CharField(max_length=50, required=False)

class AddWarehouseSheetsForInvoiceForm(forms.Form):
    invoice_id=forms.IntegerField(required=True)
    ware_house_id=forms.IntegerField(required=True)
    direction=forms.CharField(max_length=50, required=False)
    status=forms.CharField(max_length=50,required=False)

    
class AddWarehouseSheetForm(forms.Form):
    invoice_line_id=forms.IntegerField(required=True)
    ware_house_id=forms.IntegerField(required=True)
    direction=forms.CharField(max_length=50, required=False)
    status=forms.CharField(max_length=50,required=False)