from django import forms
class SearchForm(forms.Form):
    # app_name=forms.CharField(max_length=50,required=False)
    search_for=forms.CharField(max_length=500,required=True)

class DownloadMediaForm(forms.Form):
    pass

class DeletePageImageForm(forms.Form):
    page_id=forms.IntegerField(required=True)
    image_id=forms.IntegerField(required=True)

class SetThumbnailHeaderForm(forms.Form):
    page_id=forms.IntegerField(required=True)
    clear_thumbnail=forms.BooleanField(required=False)
    clear_header=forms.BooleanField(required=False)



class EncryptPageForm(forms.Form):
    page_id=forms.IntegerField(required=True)
    key=forms.CharField(max_length=200,required=False)

class DecryptPageForm(forms.Form):
    page_id=forms.IntegerField(required=True)
    key=forms.CharField(max_length=200,required=True)

class AddPageTagForm(forms.Form):
    page_id=forms.IntegerField(required=True)
    tag_title=forms.CharField(max_length=200, required=True)


class AddRelatedPageForm(forms.Form):
    page_id=forms.IntegerField(required=True)
    related_page_id=forms.IntegerField(required=True)
    bidirectional=forms.BooleanField(required=False)
    add_or_remove=forms.BooleanField(required=False)


class AddPagePermissionForm(forms.Form):
    page_id=forms.IntegerField(required=True)
    profile_id=forms.IntegerField(required=True)
    can_write=forms.BooleanField(required=False)


class ChangeParameterForm(forms.Form):
    parameter_id=forms.IntegerField(required=False)
    app_name=forms.CharField(max_length=50,required=False)
    parameter_name=forms.CharField(max_length=100,required=False)
    parameter_value=forms.CharField(max_length=10000,required=True)


class AddPageDownloadForm(forms.Form):
    page_id=forms.IntegerField(required=False)
    title=forms.CharField(max_length=50,required=False)


class AddPageLinkForm(forms.Form):
    page_id=forms.IntegerField(required=False)
    title=forms.CharField(max_length=300,required=False)
    url=forms.CharField(max_length=2000,required=False)


class TogglePageLikeForm(forms.Form):
    page_id=forms.IntegerField(required=False)


class AddPageImageForm(forms.Form):
    page_id=forms.IntegerField(required=True)
    title=forms.CharField(max_length=100, required=True)


class AddPageCommentForm(forms.Form):
    page_id=forms.IntegerField(required=True)
    comment=forms.CharField(max_length=500, required=True)


class DeletePageCommentForm(forms.Form):
    page_comment_id=forms.IntegerField(required=True)


class AddContactMessageForm(forms.Form):
    subject=forms.CharField(max_length=200, required=True)
    email=forms.CharField(max_length=50, required=True)
    mobile=forms.CharField(max_length=13, required=False)
    message=forms.CharField(max_length=500, required=True)
    full_name=forms.CharField(max_length=50, required=True)
    app_name=forms.CharField(max_length=50, required=True)
