from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout

import json
import ast # str to dict
import os

from django.utils import timezone
import pytz

from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect

from api.models import *
from forms import *

from urllib2 import urlopen
from urllib import urlencode, unquote

from chai_cloud import settings

from django.core import serializers

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

        if request.user.is_authenticated() or store_name == "api":
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

        else:
            return render(request, 'api/store-login.html', 
                {'store_name': store_name,
                 'alert': "" }) # alert text always empty on first login.

    # Handle POST requests (forms)
    if request.method == 'POST':
        #return HttpResponse(json.dumps({'here': 1}))
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
                return HttpResponse(json.dumps(active)) # for ajax calls
        
        # Update order active status to 0 when order is complete
        # Intended for AJAX calls
        if request.POST.get('complete_order'):
            form = CompleteOrder(request.POST)
            details_id = request.POST['details_id']
            print "[DEBUG] Updating status to 0 for Order Detail ID:", details_id
            selected = OrderDetail.objects.filter(id=details_id)
            selected.update(active=0)
            ws_detail_complete(details_id, store_name) # websocket update to customer
            return HttpResponse(json.dumps(details_id)) # for ajax calls

        # Store login
        if request.POST.get('username') and request.POST.get('passw'):
            form = StoreLogin(request.POST)
            username = request.POST['username']
            passw = request.POST['passw']
            store_name = request.POST['store_name']

            user = authenticate(username=username, password=passw)
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return redirect('/store-' + store_name)
                else:
                    return render(
                        request, 
                        'api/store-login.html', 
                        {'store_name': store_name,
                         'alert': "This account is disabled."})
            else:
                return render(
                    request, 
                    'api/store-login.html', 
                    {'store_name': store_name,
                     'alert': "Username and/or password is invalid."})

        # Log out
        if request.POST.get('logout'):
            logout(request)
            return HttpResponse(json.dumps({"logout": "1"}))



@csrf_exempt
def qr(request):
    """
    Generate QR code of the current store.
    URL parameters: store_id
    """
    if request.method == "GET":

        # Request for store
        if request.GET.get('store_id'):
            html_data = {'store_id': request.GET['store_id'],}
            #return render(request, 'api/qr.html', {'store_id': request.GET['store_id']})
            return render(request, 'api/qr.html', {"json": json.dumps(html_data)})
        else:
            # Incorrect parameters
            return HttpResponse(status=404)
    else:
        # Do not allow POST
        return HttpResponse(status=404)

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
        if request.POST.get('order_list') and request.POST.get('store_name'):
            #order_list = form.cleaned_data['order_list']
            response_data = {}
            # order_list format: "[{'prod_id':2, 'op_id':1},...]"
            # POST is just a string representation
            response_data['order_list'] = request.POST['order_list']
            response_data['store_name'] = request.POST['store_name']
            response_data['email'] = request.POST['email']

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
                    quantity=int(details['quantity']),
                    active=1
                ) for details in ast.literal_eval(response_data['order_list'])
            ]
            # Bulk insert
            details_create = OrderDetail.objects.bulk_create(details_list)

            # Websocket update
            order_list = ''
            for detail in details_create:
                order_list += '{"prodname":"%s", "op":"%s", "quantity":%d, "opid":%d}, ' % (
                    detail.prod.prod_name, 
                    detail.op.op_name.title(),
                    detail.quantity,
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
            #result = urlopen('http://localhost:1025', urlencode(post_data))
            result = urlopen('https://localhost:1025', urlencode(post_data))
            print "WS::::", result
            response_data['order_id'] = ord_id
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
        # check all required info is in the POST request
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

@csrf_exempt
def customer_menu(request):
    """ Retreives menu information using customer app interface. """

    # Does not allow POST request
    if request.method == "POST":
        return HttpResponse(status=404)

    if request.method == "GET":
        if request.GET.get('store_id'): # get a menu of a store

            inventory = Inventory.objects.filter(
                store_id=request.GET['store_id'], active=1)
            categories = [
                d['cat_name'] for d in Category.objects.values('cat_name')]

            
            # Build JSON response:
            # { 
            # category_name : 
            #   { 
            #   prod_name : 
            #     { 
            #     'img_url' : img_url,
            #     'prod_id' : prod_id,
            #     'prod_name' : prod_name,
            #     }, ...s
            #   }, ...
            # }
            html_data = {}
            for cat in categories:
                prod_dict = {}
                for item in inventory.filter(prod__cat__cat_name=cat):
                    prod_dict[item.prod.prod_name] = {
                        'img_url' : item.prod.img_path,
                        'prod_id' : str(item.prod_id),
                        'prod_desc': item.prod.desc,
                        'price': str(float(item.prod.price) * float(item.discount)),
                    }
                html_data[cat] = prod_dict

            return HttpResponse(json.dumps(html_data))

@csrf_exempt
def customer_product(request):
    """ Retreives product info using customer app interface. """

    # Does not allow POST request
    if request.method == "POST":
        return HttpResponse(status=404)

    if request.method == "GET":
        if request.GET.get('prod_id'):

            options = Option.objects.filter(prod_id=request.GET['prod_id'])

            # Build JSON response:
            # {
            # op_id
            #   {
            #   op_name : price
            #   }
            # }
            html_data = {}
            for option in options:
                html_data[str(option.op_id)] = {
                    option.op_name: str(option.price)
                }
            return HttpResponse(json.dumps(html_data))

@csrf_exempt
def customer_pp_token(request):
    """ Retrieves a PayPal token for checkout page. """
    if request.method == "GET":
        if request.GET.get('amt') and \
        request.GET.get('orderdetails') and \
        request.GET.get('store_id'):
            # Get store name (required for order)
            store_name = Store.objects.get(
                store_id=request.GET['store_id']).name

            # Get email for autofill (optional)
            email_str = ""
            email = settings.PP_TEST_EMAIL
            if request.GET.get('email'):
                email = request.GET['email']
                email_str = "&EMAIL=" + email

            # Call SetExpressCheckout API
            url = settings.PP_TOKEN_URL + \
                  "?USER=" + settings.PP_EMAIL + \
                  "&PWD=" + settings.PP_PSS + \
                  "&SIGNATURE=" + settings.PP_SIGNATURE + \
                  "&METHOD=SetExpressCheckout" + \
                  "&VERSION=78" + \
                  "&NOSHIPPING=1" + \
                  "&BRANDNAME=" + settings.PP_STORE_NAME + \
                  "&PAYMENTREQUEST_0_PAYMENTACTION=SALE" + \
                  "&PAYMENTREQUEST_0_AMT=" + request.GET['amt'] + \
                  "&PAYMENTREQUEST_0_CURRENCYCODE=" + settings.PP_CURRENCY + \
                  email_str + \
                  "&cancelUrl=http://www.google.com" + \
                  "&returnUrl=https://chaiapp.tk/c-status-" + store_name + \
                  "?orderdetails=" + request.GET['orderdetails']
            token_request = urlopen(url)
            return HttpResponse(
                json.dumps({'PP_SETCHECKOUT_RESPONSE': token_request.read()}))

def customer_order_status(request, store_name):
    """ 
    Return customer order status page. Intended for mobile app. 
    Must already have gotten a token from SetExpressCheckout API.
    Also creates order upon successful payment.
    """
    if request.method == "GET":
        if request.GET.get('token') and \
                request.GET.get('PayerID'):
            # Redirect from paypal successful payment
            # Call GetExpressCheckoutDetails API
            token = request.GET['token']
            details_request = pp_get_checkout_details(token)

            if "PaymentActionNotInitiated" in details_request:
                # If payment started but not done
                nvp = nvp_parse(details_request) # dict of response
                payer_id = nvp['PAYERID'] 
                amt = nvp['PAYMENTREQUEST_0_AMT'] 

                # Call DoExpressCheckout API to complete payment
                do_checkout = pp_do_checkout(payer_id, amt, token)
                finalNVP = pp_get_checkout_details(token) # NVP after checkout

                # Check payment success
                if nvp_parse(finalNVP)['CHECKOUTSTATUS'] == \
                        "PaymentActionCompleted" or \
                        nvp_parse(finalNVP)['ACK'] == "Success":

                    # Successful payment
                    
                    # Get order details
                    # order details format: "cart-<prodid>-<opid>-<quantity>cart..."
                    fname = nvp['FIRSTNAME'] # for customer reg
                    lname = nvp['LASTNAME'] # for customer reg
                    email = nvp['EMAIL'] # for customer reg + order
                    details = request.GET.get('orderdetails')#### url param
                    details = build_order(details)

                    # Check if customer exist. If not, auto register.
                    customer_sync(fname, lname, email) # register any new cust.

                    # Build url and params for order calling
                    post_data = [
                        ('order_list', details), 
                        ('store_name', store_name), 
                        ('email', email),
                    ]
                    result = urlopen(
                        settings.HTTP_URL + 'c-order', urlencode(post_data))

                    # Render customer orders status page
                    store_id = Store.objects.get(name=store_name).store_id
                    orders = Order.objects.filter(store_id=store_id)
                    customer_id = Customer.objects.get(email=nvp['EMAIL'])
                    current_orders = orders.filter(orderdetail__active=1).distinct()
                    customer_orders = current_orders.filter(cust_id=customer_id)
                    return render(
                        request, 
                        "api/order-status.html", 
                        {'customer_orders': customer_orders,
                         'store_name': store_name, 
                         'WS_URL': settings.WS_URL,})

                return HttpResponse(
                json.dumps({'BEFORE_CHECKOUT_NVP': json.dumps(nvp), 
                            'PP_GETCHECKOUT_RESPONSE': details_request,
                            'PP_DOCHECKOUT_RESPONSE': do_checkout,
                            'AFTER_CHECKOUT_NVP': finalNVP,}))
            else:
                # Not coming from a payment page (mostly for testing)
                # Render customer order status
                store_id = Store.objects.get(name=store_name).store_id
                orders = Order.objects.filter(store_id=store_id)
                nvp = nvp_parse(details_request) # dict of response
                customer_id = Customer.objects.get(email=nvp['EMAIL'])
                current_orders = orders.filter(orderdetail__active=1).distinct()
                customer_orders = current_orders.filter(cust_id=customer_id)
                return render(
                    request, 
                    "api/order-status.html", 
                    {'customer_orders': customer_orders,
                     'store_name': store_name, 
                     'WS_URL': settings.WS_URL,})


####################
# Helper functions
####################

def ws_detail_complete(detail_id, store_name):
    """
    Websocket update to customer app when an order detail is complete.
    """
    order_id = OrderDetail.objects.get(id=detail_id).ord_id
    post_str = "{\"action\":\"detail_complete\"," + \
       " \"detail_id\":\"%s\"," % detail_id + \
       " \"order_id\":\"%s\"," % order_id + \
       " \"store_name\":\"%s\" }" % store_name
    post_data = [('new_message', post_str),]
    result = urlopen('https://localhost:1025', urlencode(post_data))
    print "WS::::", result

@csrf_exempt
def build_order(orderdetails):
    """
    Return json string for orderdetails ready for order calling.
    Params:
    orderdetails: string in format "cart-<prodid>-<ordid>-<quantity>cart..."
    """
    out = ""
    cart = orderdetails.split("cart-")
    for item in cart:
        if len(item) > 1: # exclude first "" from "cart-split"
            item_split = item.split("-")
            out += "{'prod_id': %s, 'op_id':%s, 'quantity':%s}, " % \
                   (item_split[0], item_split[1], item_split[2])
    out = "[%s]" % out[:-2]
    return out

@csrf_exempt
def nvp_parse(nvp_str):
    """ Return json dictionary of NVP string. """
    out = dict()
    pairs = nvp_str.split("&")
    for pair in pairs:
        # NVP is URL encoded, must use unquote
        out[pair.split("=")[0]] = unquote(pair.split("=")[1])
    return out

@csrf_exempt
def customer_sync(fname, lname, email):
    """
    Check if customer exist in database. If not, create a customer.
    """
    customer = Customer.objects.filter(email=email)
    if not customer:
        new_customer = Customer.objects.create(
            fname = fname,
            lname = lname,
            email = email)

@csrf_exempt
def pp_do_checkout(payer_id, amt, token):
    """ 
    Call PayPal DoExpressCheckoutPayment API and return response string.
    Reference: 
    https://developer.paypal.com/docs/classic/api/merchant/DoExpressCheckoutPayment_API_Operation_NVP/
    """
    url = settings.PP_TOKEN_URL + \
          "?USER=" + settings.PP_EMAIL + \
          "&PWD=" + settings.PP_PSS + \
          "&SIGNATURE=" + settings.PP_SIGNATURE + \
          "&METHOD=DoExpressCheckoutPayment" + \
          "&TOKEN=" + token + \
          "&VERSION=78" + \
          "&PAYERID=" + payer_id + \
          "&PAYMENTREQUEST_0_AMT=" + amt + \
          "&PAYMENTREQUEST_0_CURRENCYCODE=" + settings.PP_CURRENCY + \
          "&PAYMENTREQUEST_0_PAYMENTACTION=Sale"
    checkout_request = urlopen(url)
    return checkout_request.read()

@csrf_exempt
def pp_get_checkout_details(token):
    """ 
    Call PayPal GetExpressCheckoutDetails API and return response string.
    Reference: 
    https://developer.paypal.com/docs/classic/api/merchant/GetExpressCheckoutDetails_API_Operation_NVP/
    """
    url = settings.PP_TOKEN_URL + \
          "?USER=" + settings.PP_EMAIL + \
          "&PWD=" + settings.PP_PSS + \
          "&SIGNATURE=" + settings.PP_SIGNATURE + \
          "&METHOD=GetExpressCheckoutDetails" + \
          "&TOKEN=" + token + \
          "&VERSION=78"
    details_request = urlopen(url)
    return details_request.read()

@csrf_exempt
def ssl_check(request):
    """ SSL certificate verification file for cheapsslsecurity.com """
    return render(request, 'api/e9b14fld.htm',)

@csrf_exempt
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
        quantity = random.randint(1,5)
        order_str += "{'prod_id': %d, 'op_id':%d, 'quantity':%d}, " % \
                     (prod_id, op_id, quantity)
    order_str = "[%s]" % order_str[:-2]
    #print ":::::: i got here"
    # POST call
    post_data = [
        ('order_list', order_str), 
        ('store_name', store_name), 
        ('email', email),
    ]
    result = urlopen(settings.HTTP_URL + 'c-order', urlencode(post_data))



