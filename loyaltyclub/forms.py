from django import forms

class AddOrderForm(forms.Form):
    date_ordered=forms.CharField( max_length=100, required=False)
    title=forms.CharField( max_length=100, required=True)
    supplier_id=forms.IntegerField(required=True)
    customer_id=forms.IntegerField(required=True)
    invoice_id=forms.IntegerField(required=False)
    sum=forms.IntegerField(required=True)
    ship_fee=forms.IntegerField(required=False)
    discount=forms.IntegerField(required=False)
    coupon=forms.IntegerField(required=False)


class ChangeCoefForm(forms.Form):
    number=forms.IntegerField(required=True)
    percentage=forms.IntegerField(required=True)