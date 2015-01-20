from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse

import json
import ast # str to dict
from django.utils import timezone

from django.shortcuts import render
from django.http import HttpResponseRedirect

from api.models import *
from api.serializers import APISerializer, StoreSerializer, InventorySerializer

from forms import *

class JSONResponse(HttpResponse):
    """ JSON rendered HTTP response. """

    def __init__(self, data, **kwargs):
        content = JSONRenderer().render(data)
        kwargs['content_type'] = 'application/json'
        super(JSONResponse, self).__init__(content, **kwargs)

##########################
# Store views
##########################

@csrf_exempt
def store_view(request, store_name):
    """
    Storefront view for employees operating the store, 
    handles all GET/POST requests and renders in HTML.
    """
    # Handle GET requests
    if request.method == "GET":

        # Lists all orders and store inventory
        store_id = Store.objects.get(name=store_name).store_id
        inventory = Inventory.objects.filter(store_id=store_id)
        orders = Order.objects.filter(store_id=store_id)
        current_orders = orders.filter(orderdetail__active=1).distinct()
        form = InventoryActiveForm() # empty form for GET requests
        html_data = {'inventory': inventory,
                     'orders': orders,
                     'current_orders': current_orders,
                     'store_name': store_name,
                     'store_id': store_id,
                     'empty_form': form}
        return render(request, 'api/stores.html', html_data)

    # Handle POST requests (forms)
    if request.method == 'POST':

        # Updates active/inactive status of inventory item
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
        
        # Update order active status to 0 when order is complete
        if request.POST.get('complete_order'):
            form = CompleteOrder(request.POST)
            details_id = request.POST['details_id']
            selected = OrderDetail.objects.filter(id=details_id)
            selected.update(active=0)
            return HttpResponseRedirect('/store-%s' % store_name)


##########################
# Customer views
##########################

@csrf_exempt
def customer_order(request):

    # Does not allow GET request
    if request.method == "GET":
        return HttpResponse(status=404)
    
    # Handle POST requests 
    if request.method == "POST":
        # New orders
        #return HttpResponse(request.POST.get('order_list'))
        if request.POST.get('order_list') and request.POST.get('store_name'):
            #order_list = form.cleaned_data['order_list']
            response_data = {}
            # order_list format: "[{'prod_id':2, 'op_id':1},...]"
            # POST is just a string representation
            response_data['order_list'] = request.POST['order_list']
            response_data['store_name'] = request.POST['store_name']
            response_data['email'] = request.POST['email']
            #response_data['time'] = timezone.now()

            #response_data={"a": request.POST['order_list']}
            #response_data['order_list'] = ast.literal_eval(
            #                                request.POST['order_list'])

            # Add order to DB (one order can have serveral products)
            store_id = Store.objects.get(
                name=response_data['store_name']).store_id
            cust_id = Customer.objects.get(
                email=response_data['email']).cust_id
            order_create = Order.objects.create(
                store_id=store_id, 
                cust_id=cust_id,
                time=timezone.now()
            )
            #order_create.save()

            # Add order details to DB (individual products per order)
            # Create list of products models
            details_list = [
                OrderDetail(
                    ord_id=order_create.ord_id,
                    prod_id=int(details['prod_id']),
                    op_id=int(details['op_id']),
                    active=1
                ) for details in ast.literal_eval(response_data['order_list'])
            ]
            # Bulk insert
            details_create = OrderDetail.objects.bulk_create(details_list)

            return HttpResponse(json.dumps(response_data), 
                                content_type="application/json")















