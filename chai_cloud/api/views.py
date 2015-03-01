from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse

import json
import ast # str to dict
import os

from django.utils import timezone
import pytz

from django.shortcuts import render
from django.http import HttpResponseRedirect

from api.models import *
from forms import *

from urllib2 import urlopen
from urllib import urlencode

from chai_cloud import settings

import sqlite3
import random

import bcrypt

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
        # Render: HTML
        store_id = Store.objects.get(name=store_name).store_id
        inventory = Inventory.objects.filter(store_id=store_id)
        orders = Order.objects.filter(store_id=store_id)
        current_orders = orders.filter(orderdetail__active=1).distinct()
        websocket_url = settings.WS_URL
        form = InventoryActiveForm() # empty form for GET requests
        html_data = {'inventory': inventory,
                     'orders': orders,
                     'WS_URL': websocket_url,
                     'current_orders': current_orders,
                     'store_name': store_name,
                     'store_id': store_id,
                     'empty_form': form}
        return render(request, 'api/stores.html', html_data)

    # Handle POST requests (forms)
    if request.method == 'POST':

        # Updates active/inactive status of inventory item
        # Intended for AJAX calls
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
                #return HttpResponseRedirect('/store-%s' % store_name) # for html views
                return HttpResponse(json.dumps(active)) # for ajax calls
        
        # Update order active status to 0 when order is complete
        # Intended for AJAX calls
        if request.POST.get('complete_order'):
            form = CompleteOrder(request.POST)
            details_id = request.POST['details_id']
            print "[DEBUG] Updating status to 0 for Order Detail ID:", details_id
            selected = OrderDetail.objects.filter(id=details_id)
            selected.update(active=0)
            #return HttpResponseRedirect('/store-%s' % store_name) # for html views
            return HttpResponse(json.dumps(details_id)) # for ajax calls



##########################
# Customer views
##########################

@csrf_exempt
def customer_order(request):
    """
    Take customer orders through HTTP POST requests from customer app.
    """

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
            ord_id = order_create.ord_id
            #order_create.save()

            # Add order details to DB (individual products per order)
            # Create list of products models
            details_list = [
                OrderDetail(
                    ord_id=ord_id,
                    prod_id=int(details['prod_id']),
                    op_id=int(details['op_id']),
                    active=1
                ) for details in ast.literal_eval(response_data['order_list'])
            ]
            # Bulk insert
            details_create = OrderDetail.objects.bulk_create(details_list)

            # Websocket update
            order_list = ''
            for detail in details_create:
                order_list += '{"prodname":"%s", "op":"%s", "opid":%d}, ' % (
                    detail.prod.prod_name, 
                    detail.op.op_name.title(),
                    OrderDetail.objects.get( # order detail id
                        ord_id=detail.ord_id,
                        prod_id=detail.prod_id,
                        op_id=detail.op_id,
                        active=1).id,
                )

            # list of orders formatted for output
            order_list = "[%s]" % order_list[:-2] # get rid of trailing comma/space
            # send websocket POST
            post_str = "{\"action\":\"order\"," + \
               " \"orderlist\":%s," % order_list + \
               " \"storename\":\"%s" % request.POST['store_name'] + \
               "\", \"customer\":\"%s %s\"," % (
                    Customer.objects.get(
                        email=response_data['email']).fname,
                    Customer.objects.get(
                        email=response_data['email']).lname) + \
               " \"custid\":%d, " % cust_id + \
               "\"ordertime\":\"%s\"," % \
                    Order.objects.get(ord_id=ord_id).time.astimezone(
                        pytz.timezone('US/Eastern')).strftime(
                        "%I:%M %p") + \
               " \"orderid\":%d}" % ord_id
            post_data = [('new_message', post_str),]
            result = urlopen('http://localhost:1025', urlencode(post_data))
            return HttpResponse(json.dumps(response_data), 
                                content_type="application/json")

        # Generate one customer order from the store view
        # Used only for demo purposes
        # Intended for AJAX calls
        if request.POST.get("generate_orders") \
                    and request.POST.get("store_name"):
            #os.system(
            #    "python _customer_simulate.py %s" % request.POST['store_name']
            #)
            print ":::::randorder for", request.POST['store_name']
            random_order(request.POST['store_name'])
            return HttpResponse(json.dumps(request.POST['store_name']))

@csrf_exempt
def customer_register(request):
    """ Creates new customer account. """

    # Does not allow GET request
    if request.method == "GET":
        return HttpResponse(status=404)

    if request.method == "POST":
        if request.POST.get('email') and \
                    request.POST.get('pass') and \
                    request.POST.get('fname') and \
                    request.POST.get('lname'):
            hashed = bcrypt.hashpw(request.POST['pass'].encode('utf-8'), bcrypt.gensalt())
            register = Customer.objects.create(
                fname=request.POST['fname'],
                lname=request.POST['lname'],
                email=request.POST['email'],
                passhash=hashed)
            return HttpResponse(json.dumps({'status':'registered'}), 
                                content_type="application/json")


####################
# Helper functions
####################
def random_order(store_name):
    """
    Add an order to a store with a random customer, random inventory item.
    Uses HTTP POST request to localhost:8000.
    """
    conn = sqlite3.connect(settings.DATABASES['default']['NAME'])
    cur = conn.cursor()

    # Get random customer email
    cur.execute("select max(cust_id) from Customer")
    max_id = cur.fetchone()[0]
    cur.execute(
        "select email from Customer where cust_id=?", 
        (random.randint(1,max_id),)
    )
    email = cur.fetchone()[0]

    # Generate random order list of 1-5 items
    cur.execute(
        "select store_id from Store where name=?",
        (store_name,)
    )
    store_id = cur.fetchone()[0]
    print "store_id::::", store_id
    cur.execute(
        "select prod_id from Inventory where active=1 and store_id=?",
        (store_id,)
    )
    raw_list = cur.fetchall()
    # edge case: less than 5 active items
    max_length = [5, len(raw_list)][len(raw_list) < 5]
    if not max_length:
        print "[DEBUG] No active items in: %s. Cannot make orders." % \
               store_name
        return 0
    prod_id_list = random.sample(
        [i[0] for i in raw_list],
        random.randint(1,max_length)
    )
    
    order_str = "" # string format for order list
    for prod_id in prod_id_list:
        # Get random option for each product
        cur.execute(
            "select op_id from Option where prod_id=?",
            (prod_id,)
        )
        op_id = random.choice([i[0] for i in cur.fetchall()])
        order_str += "{'prod_id': %d, 'op_id':%d}, " % (prod_id, op_id)
    order_str = "[%s]" % order_str[:-2]
    
    # POST call
    post_data = [
        ('order_list', order_str), 
        ('store_name', store_name), 
        ('email', email),
    ]
    result = urlopen(settings.HTTP_URL + 'order', urlencode(post_data))



