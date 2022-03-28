from django import forms


class ChangeWarehouseSheetStateForm(forms.Form):
    warehouse_sheet_id=forms.IntegerField(required=True)
    status=forms.CharField(max_length=50, required=True)
     