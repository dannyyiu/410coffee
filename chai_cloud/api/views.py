from rest_framework import viewsets, routers
from rest_framework import status

from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse

from rest_framework.decorators import api_view

from django.shortcuts import render
from django.http import HttpResponseRedirect

from api.models import *
from api.serializers import APISerializer, StoreSerializer, InventorySerializer

from rest_framework.response import Response 

from forms import InventoryActiveForm

class PhotoViewSet(viewsets.ModelViewSet):
    model = Photo
    queryset = Photo.objects.all()
    serializer_class = APISerializer
    #permission_classes = (IsAuthenticatedOrReadOnly,)

    def get_queryset(self):
        print self.request.user
        return Photo.objects.all()
 
    def list(self, request, *args, **kwargs):
        return Response({"name": str(request.user)})
    def create(self, request, *args, **kwargs):
        if str(request.user) == 'dan':
            return Response({"user": str(request.user)})
        return Response({"error": str(request.user)})

#class StoreViewSet(viewsets.ModelViewSet):
#    model = Store
#    serializer_class = InventorySerializer
#
#    def update(self, request, *args, **kwargs):
#        queryset = Inventory.objects.all()
#        #permissionclasses = (permissions.IsAuthenticatedOrReadOnly)
#        return self.update(request, *args, **kwargs)
#
#    def list(self, request, *args, **kwargs):
#        store_name = kwargs['store_name']
#        queryset = Store.objects.all()
#        inventory = Inventory.objects.all()
#        orders = Order.objects.all()
#
#        html_data = {'data': queryset,
#                     'inventory': inventory,
#                     'orders': orders,
#                     'store_name': kwargs['store_name']}
#        #serializer = StoreSerializer(queryset, many=True)
#        #return Response(serializer.data)
#        return Response(html_data, template_name='api/stores.html')

@csrf_exempt
def store_view(request, store_name):
    if request.method == "GET":
        inventory = Inventory.objects.all()
        orders = Order.objects.all()
        form = InventoryActiveForm() # empty form
        html_data = {'inventory': inventory,
                     'orders': orders,
                     'store_name': store_name}
        return render(request, 'api/stores.html', html_data)
    if request.method == 'POST':
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

 
# Register the viewset
api_router = routers.DefaultRouter()
api_router.register(r'k/photo', PhotoViewSet)
#api_router.register(r'store-(?P<store_name>[a-zA-Z]+)', store_view) # default page
#api_router.register(r'inventory', DevViewSet)
#api_router.register(r'order', DevViewSet)