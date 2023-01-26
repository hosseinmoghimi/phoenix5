from django import forms

class AddGuaranteeForm(forms.Form):
    start_date=forms.CharField(max_length=50, required=True)
    end_date=forms.CharField(max_length=50, required=True)
    status=forms.CharField(max_length=50, required=False)
    type=forms.CharField(max_length=50, required=False)
    serial_no=forms.CharField(max_length=5000, required=True)
    invoice_line_id=forms.IntegerField(required=True)