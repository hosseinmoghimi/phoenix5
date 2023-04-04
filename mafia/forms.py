from django import forms

class AddRoleForm(forms.Form):
    title=forms.CharField(max_length=50, required=True)
    side=forms.CharField(max_length=50, required=True)
    description=forms.CharField(max_length=5000, required=False)

class AddRoleToGameForm(forms.Form):
    game_id=forms.IntegerField(required=True)
    role_id=forms.IntegerField(required=True)
    
class AddPlayerForm(forms.Form):
    account_id=forms.IntegerField(required=True) 
    
class AddGodForm(forms.Form):
    account_id=forms.IntegerField(required=True) 
    
class InitializeForm(forms.Form):
    title=forms.CharField(max_length=50, required=False)

class AddRolePlayerForm(forms.Form):
    title=forms.CharField(max_length=50, required=True)
    description=forms.CharField(max_length=5000, required=False)

class AddPlayerToGameForm(forms.Form):
    game_id=forms.IntegerField(required=True)
    role_id=forms.IntegerField(required=True)
    player_id=forms.IntegerField(required=True)

class AddGameForm(forms.Form):
    # title=forms.CharField(max_length=50, required=False)
    game_scenario_id=forms.IntegerField (required=True)
    god_id=forms.IntegerField (required=True)
    description=forms.CharField(max_length=5000, required=False)