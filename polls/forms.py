from django import forms

class AddPollForm(forms.Form):
    title=forms.CharField( max_length=500, required=True)

class AddOptionForm(forms.Form):
    title=forms.CharField( max_length=500, required=True)
    poll_id=forms.IntegerField(required=True)