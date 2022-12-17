from django import forms
class SearchForm(forms.Form):
    search_for=forms.CharField(max_length=50, required=True)


class AddBrandForm(forms.Form):
    title=forms.CharField(max_length=100, required=True)


class AddCustomerForm(forms.Form):
    account_id=forms.IntegerField(required=True)
    region_id=forms.IntegerField(required=True)
    
class CheckoutForm(forms.Form):
    customer_id=forms.IntegerField(required=True)
    cart_lines=forms.CharField(max_length=2000, required=False)

class AddShopForm(forms.Form):
    supplier_id=forms.IntegerField(required=True)
    product_id=forms.IntegerField( required=True)
    specifications=forms.CharField(max_length=2000, required=False)
    unit_name=forms.CharField(required=True)
    old_price=forms.CharField(required=False)
    buy_price=forms.CharField(required=False)
    level=forms.CharField(required=False)
    unit_price=forms.IntegerField(required=True)
    available=forms.IntegerField(required=False)

class AddToCartForm(forms.Form):
    shop_id=forms.IntegerField(required=True)
    quantity=forms.IntegerField(required=True)
    description=forms.CharField(max_length=1000, required=False)


class AddExistingProductToCategoryForm(forms.Form):
    product_id=forms.IntegerField(required=True)
    category_id=forms.IntegerField(required=True)
    add=forms.BooleanField(required=True)
    
class AddCategoryForm(forms.Form):
    title=forms.CharField(max_length=50, required=True)
    parent_id=forms.IntegerField( required=False)

class AddProductForm(forms.Form):
    title=forms.CharField(max_length=100, required=True)
    category_id=forms.IntegerField( required=False)
