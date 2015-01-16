from rest_framework import viewsets, routers
from api.models import *
from api.serializers import APISerializer, StoresSerializer

from rest_framework.response import Response 

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

class DevViewSet(viewsets.ViewSet):
    model = Stores
    def list(self, request, *args, **kwargs):
        store_name = kwargs['store_name']
        queryset = Stores.objects.all()
        inventory = Inventory.objects.all()
        order = Order.objects.all()
        orderdetail = OrderDetail.objects.all()

        html_data = {'data': queryset,
                     'inventory': inventory,
                     'order':order,
                     'orderdetail': orderdetail,
                     'store_name': kwargs['store_name']}
        #serializer = StoresSerializer(queryset, many=True)
        #return Response(serializer.data)
        return Response(html_data, template_name='stores.html')


 
# Register the viewset
api_router = routers.DefaultRouter()
api_router.register(r'k/photo', PhotoViewSet)
api_router.register(r'store-(?P<store_name>[a-zA-Z]+)', DevViewSet) # default page
api_router.register(r'inventory', DevViewSet)
api_router.register(r'order', DevViewSet)