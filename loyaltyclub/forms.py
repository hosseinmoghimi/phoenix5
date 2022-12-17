from django import forms

class AddOrderForm(forms.Form):
    date_ordered=forms.CharField( max_length=100, required=False)
    title=forms.CharField( max_length=100, required=True)
    customer_id=forms.IntegerField(required=True)
    invoice_id=forms.IntegerField(required=False)
    sum=forms.IntegerField(required=True)