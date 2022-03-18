from django import forms

class SearchFrom(forms.Form):
    search_for=forms.CharField( max_length=200, required=True)
    
class AddStorePriceForm(forms.Form):
    productorservice_id=forms.IntegerField(required=True)
    store_id=forms.IntegerField(required=True)
    sell_price=forms.IntegerField(required=True)
    buy_price=forms.IntegerField(required=True)


class GetReportForm(forms.Form):
    financial_account_id=forms.IntegerField(required=True)
    start_date=forms.CharField(max_length=50, required=True)
    end_date=forms.CharField(max_length=50, required=True)

class AddFinancialDocumentForm(forms.Form):
    title=forms.CharField( max_length=200, required=True)
    document_datetime=forms.CharField(max_length=20, required=True)
    bestankar=forms.IntegerField(required=True)
    account_id=forms.IntegerField(required=True)
    bedehkar=forms.IntegerField(required=True)
    category_id=forms.IntegerField(required=True)
class SearchForm(forms.Form):
    search_for=forms.CharField( max_length=500, required=True)

class AddChequeForm(forms.Form):
    title=forms.CharField( max_length=500, required=True)
    
class AddPriceForm(forms.Form):
    item_id=forms.IntegerField(required=True)
    sell_price=forms.IntegerField(required=True)
    buy_price=forms.IntegerField(required=True)
    account_id=forms.IntegerField(required=False)
    
class AddPaymentForm(forms.Form):
    title=forms.CharField( max_length=500, required=True)
    pay_to_id=forms.IntegerField(required=True)
    pay_from_id=forms.IntegerField(required=True)
    amount=forms.IntegerField(required=True)
    transaction_datetime=forms.CharField( max_length=50, required=True)
    payment_method=forms.CharField( max_length=50, required=True)
    description=forms.CharField( max_length=50, required=False)
class EditInvoiceForm(forms.Form):
    invoice_id=forms.IntegerField(required=True)
    discount=forms.IntegerField(required=True)
    lines=forms.CharField(max_length=50000, required=True)
    description=forms.CharField(max_length=5000, required=False)
    invoice_datetime=forms.CharField(max_length=20, required=True)
    pay_to_id=forms.IntegerField(required=True)
    pay_from_id=forms.IntegerField(required=True)
    tax_percent=forms.IntegerField(required=True)
    ship_fee=forms.IntegerField(required=True)
    status=forms.CharField(max_length=50, required=True)
    payment_method=forms.CharField(max_length=50, required=True)
class ChangeWarehouseSheetStateForm(forms.Form):
    warehouse_sheet_id=forms.IntegerField(required=True)
    status=forms.CharField(max_length=50, required=True)
    
class AddCostForm(forms.Form):
    # cost_type=forms.IntegerField(required=True)
    # amount=forms.IntegerField(required=True)
    # cost_date=forms.CharField(max_length=50, required=True)
    # status=forms.CharField(max_length=50, required=False)
    amount=forms.IntegerField(required=True)
    cost_type=forms.CharField( max_length=100, required=True)
    description=forms.CharField( max_length=50, required=False)
    pay_from_id=forms.IntegerField(required=True)
    pay_to_id=forms.IntegerField(required=True)
    payment_method=forms.CharField( max_length=50, required=True)
    title=forms.CharField( max_length=500, required=True)
    transaction_datetime=forms.CharField( max_length=50, required=True)

class AddWageForm(forms.Form):
    # cost_type=forms.IntegerField(required=True)
    # amount=forms.IntegerField(required=True)
    # cost_date=forms.CharField(max_length=50, required=True)
    # status=forms.CharField(max_length=50, required=False)
    amount=forms.IntegerField(required=True)
    description=forms.CharField( max_length=50, required=False)
    pay_from_id=forms.IntegerField(required=True)
    pay_to_id=forms.IntegerField(required=True)
    payment_method=forms.CharField( max_length=50, required=True)
    title=forms.CharField( max_length=500, required=True)
    transaction_datetime=forms.CharField( max_length=50, required=True)
class AddTransactionDocumentForm(forms.Form):
    transaction_id=forms.IntegerField(required=True)
    title=forms.CharField( max_length=50, required=True)
class AddTransactionLinkForm(forms.Form):
    transaction_id=forms.IntegerField(required=True)
    title=forms.CharField( max_length=500000, required=True)
    url=forms.CharField( max_length=500000, required=True)
    