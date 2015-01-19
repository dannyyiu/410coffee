from django import forms

class InventoryActiveForm(forms.Form):
    active = forms.IntegerField()
    prod_id = forms.IntegerField()
    store_id = forms.IntegerField()