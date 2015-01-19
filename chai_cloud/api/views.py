from rest_framework import viewsets, routers
from api.models import *
from api.serializers import APISerializer, StoreSerializer

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

class StoreViewSet(viewsets.ViewSet):
    model = Store

    def list(self, request, *args, **kwargs):
        store_name = kwargs['store_name']
        queryset = Store.objects.all()
        inventory = Inventory.objects.all()
        orders = Order.objects.all()

        html_data = {'data': queryset,
                     'inventory': inventory,
                     'orders': orders,
                     'store_name': kwargs['store_name']}
        #serializer = StoreSerializer(queryset, many=True)
        #return Response(serializer.data)
        return Response(html_data, template_name='api/stores.html')


 
# Register the viewset
api_router = routers.DefaultRouter()
api_router.register(r'k/photo', PhotoViewSet)
api_router.register(r'store-(?P<store_name>[a-zA-Z]+)', StoreViewSet) # default page
api_router.register(r'inventory', DevViewSet)
api_router.register(r'order', DevViewSet)