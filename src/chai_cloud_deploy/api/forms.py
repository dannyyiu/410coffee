from django import forms

class InventoryActiveForm(forms.Form):
    """
    POST from store for inventory status update.
    """
    active = forms.IntegerField()
    prod_id = forms.IntegerField()
    store_id = forms.IntegerField()

class CompleteOrder(forms.Form):
    """
    POST from store to complete order.
    """
    details_id = forms.IntegerField()
    complete_order = forms.CharField()

class StoreLogin(forms.Form):
    """
    POST from store login page.
    """
    username = forms.CharField()
    passw = forms.CharField()