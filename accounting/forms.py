from django import forms
class SearchForm(forms.Form):
    search_for=forms.CharField( max_length=200, required=False)
    start_date=forms.CharField(max_length=20, required=False)
    end_date=forms.CharField(max_length=20, required=False)
    account_id=forms.IntegerField(required=False)
    profile_id=forms.IntegerField(required=False)


class AddAccountTagForm(forms.Form):
    tag=forms.CharField(max_length=100, required=False)
    account_id=forms.IntegerField(required=False)

class AddBankAccountForm(forms.Form):
    title=forms.CharField(max_length=50, required=False)
    shaba_no=forms.CharField(max_length=50, required=False)
    account_no=forms.CharField(max_length=20, required=False)
    card_no=forms.CharField(max_length=16, required=False)
    account_id=forms.IntegerField(required=False)
    bank_id=forms.IntegerField(required=False)
    is_default=forms.BooleanField(required=False)

class AddBankForm(forms.Form):
    name=forms.CharField( max_length=200, required=True)
    branch=forms.CharField( max_length=200, required=False)
    tel=forms.CharField(max_length=20, required=False)
    address=forms.CharField(max_length=20, required=False)

class TransactionsPrintForm(forms.Form):
    title=forms.CharField(max_length=200, required=True)
    transactions=forms.CharField( max_length=5000, required=True)


class AddAccountForm(forms.Form):
    title=forms.CharField(max_length=200, required=False)
    balance=forms.IntegerField(required=False)
    address=forms.CharField(max_length=100,required=False)
    tel=forms.CharField(max_length=50,required=False)
    mobile=forms.CharField(max_length=50,required=False)
    description=forms.CharField(max_length=500, required=False)
    
class AddFinancialBalanceForm(forms.Form):
    title=forms.CharField(max_length=50, required=True)
    financial_document_id=forms.IntegerField(required=True)
    bedehkar=forms.IntegerField(required=False)
    bestanker=forms.IntegerField(required=False)
    amount=forms.IntegerField(required=False)

class AddProductSpecificationForm(forms.Form):
    product_id=forms.IntegerField(required=True)
    name=forms.CharField(max_length=200,required=True)
    value=forms.CharField(max_length=200,required=True)


class AddProductOrServiceUnitNameForm(forms.Form):
    product_or_service_id=forms.IntegerField(required=True)
    unit_name=forms.CharField(max_length=200,required=True)
    coef=forms.IntegerField(required=False)
    
class AddStorePriceForm(forms.Form):
    product_or_service_id=forms.IntegerField(required=True)
    store_id=forms.IntegerField(required=True)
    sell_price=forms.IntegerField(required=True)
    buy_price=forms.IntegerField(required=True)
 
class CreateAccountForm(forms.Form):
    profile_id=forms.IntegerField(required=False)

class AddProductForm(forms.Form):
    category_id=forms.IntegerField(required=False)
    title=forms.CharField(max_length=500,required=True)

class PrintTransactionForm(forms.Form):
    transaction_id=forms.IntegerField(required=False)
    
class RollBackTransactionForm(forms.Form):
    transaction_id=forms.IntegerField(required=False)
    

class AddServiceForm(forms.Form):
    title=forms.CharField(max_length=500,required=True)

    
class GetReportForm(forms.Form):
    account_id=forms.IntegerField(required=False)
    amount=forms.IntegerField(required=False)
    search_for=forms.CharField(max_length=50, required=False)
    payment_method=forms.CharField(max_length=50, required=False)
    status=forms.CharField(max_length=50, required=False)
    start_date=forms.CharField(max_length=50, required=False)
    end_date=forms.CharField(max_length=50, required=False)


class AddFinancialDocumentForm(forms.Form):
    title=forms.CharField( max_length=200, required=True)
    bestankar=forms.IntegerField(required=True)
    account_id=forms.IntegerField(required=True)
    bedehkar=forms.IntegerField(required=True)
    category_id=forms.IntegerField(required=True)
 

class AddChequeForm(forms.Form):
    title=forms.CharField( max_length=500, required=True)
    pay_from_id=forms.IntegerField(required=True)
    pay_to_id=forms.IntegerField(required=True)
    amount=forms.IntegerField(required=True)
    description=forms.CharField( max_length=500, required=False)
    status=forms.CharField( max_length=50, required=False)
    sayyad_no=forms.CharField( max_length=50, required=True)
    sarresid_datetime=forms.CharField( max_length=50, required=True)
    transaction_datetime=forms.CharField( max_length=50, required=True)
    serial_no=forms.CharField( max_length=50, required=True)
    bank_id=forms.IntegerField(required=True)



class AddPriceForm(forms.Form):
    unit_name=forms.CharField(required=False,max_length=50)
    product_or_service_id=forms.IntegerField(required=True)
    sell_price=forms.IntegerField(required=True)
    buy_price=forms.IntegerField(required=True)
    account_id=forms.IntegerField(required=False)
 
    
class AddPaymentForm(forms.Form):
    title=forms.CharField(max_length=500, required=True)
    pay_to_id=forms.IntegerField(required=True)
    pay_from_id=forms.IntegerField(required=True)
    amount=forms.IntegerField(required=True)
    payment_datetime=forms.CharField(max_length=50, required=True)
    payment_method=forms.CharField(max_length=50, required=True)
    status=forms.CharField(max_length=50, required=False)
    description=forms.CharField(max_length=200, required=False)

    
class EditInvoiceForm(forms.Form):
    invoice_id=forms.IntegerField(required=True)
    discount=forms.IntegerField(required=True)
    title=forms.CharField(max_length=300, required=True)
    lines=forms.CharField(max_length=50000, required=True)
    description=forms.CharField(max_length=5000, required=False)
    invoice_datetime=forms.CharField(max_length=20, required=True)
    pay_to_id=forms.IntegerField(required=True)
    pay_from_id=forms.IntegerField(required=True)
    tax_percent=forms.IntegerField(required=True)
    ship_fee=forms.IntegerField(required=True)
    status=forms.CharField(max_length=50, required=True)
    payment_method=forms.CharField(max_length=50, required=True)


class AddCostForm(forms.Form):
    amount=forms.IntegerField(required=True)
    cost_type=forms.CharField( max_length=100, required=True)
    description=forms.CharField( max_length=500, required=False)
    pay_from_id=forms.IntegerField(required=True)
    payment_method=forms.CharField( max_length=50, required=True)
    transaction_datetime=forms.CharField( max_length=50, required=True)
    status=forms.CharField( max_length=100, required=False)
    title=forms.CharField(max_length=500, required=True)


class AddProductOrServiceCategoryForm(forms.Form):
    parent_id=forms.IntegerField(required=False)
    title=forms.CharField(max_length=100, required=True)

    
class AddItemCategoryForm(forms.Form):
    category_id=forms.IntegerField(required=False)
    product_or_service_id=forms.IntegerField(required=False)


class AddCategoryForm(forms.Form):
    parent_id=forms.IntegerField(required=False)
    title=forms.CharField(max_length=100, required=True)


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
    