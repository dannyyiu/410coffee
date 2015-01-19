from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse

from django.shortcuts import render
from django.http import HttpResponseRedirect

from api.models import *
from api.serializers import APISerializer, StoreSerializer, InventorySerializer

from forms import InventoryActiveForm

@csrf_exempt
def store_view(request, store_name):
    """
    Storefront view for employees operating the store, handles all GET/POST requests
    and renders in HTML.
    """
    if request.method == "GET":
        inventory = Inventory.objects.all()
        orders = Order.objects.all()
        form = InventoryActiveForm() # empty form for GET requests
        html_data = {'inventory': inventory,
                     'orders': orders,
                     'store_name': store_name}
        return render(request, 'api/stores.html', html_data)

    if request.method == 'POST':

        if request.POST.get('active'):
            form = InventoryActiveForm(request.POST)
            if form.is_valid():
                inventory = Inventory.objects.all()
                prod_id = form.cleaned_data['prod_id']
                store_id = form.cleaned_data['store_id']
                active = form.cleaned_data['active']
                selected = Inventory.objects.filter(
                    prod_id=prod_id).filter(
                    store_id=store_id)
                selected.update(active=active)
                return HttpResponseRedirect('/store-%s' % store_name)
