from django import forms
class SearchForm(forms.Form):
    search_for=forms.CharField(max_length=50, required=True)


class AddBrandForm(forms.Form):
    title=forms.CharField(max_length=100, required=True)


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
