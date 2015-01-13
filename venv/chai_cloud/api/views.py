#from django.shortcuts import render

## imports for default httpresponse class
#from django.http import HttpResponse
#from django.views.decorators.csrf import csrf_exempt
#from rest_framework.renderers import JSONRenderer
#from rest_framework.parsers import JSONParser

# imports for generic based views
from rest_framework import generics

## imports for mixins
#from rest_framework import mixins
#from rest_framework import generics

## imports for APIView
#from rest_framework.views import APIView
#from rest_framework.response import Response
#from rest_framework import status

## imports for rest response class
#from rest_framework import status
#from rest_framework.decorators import api_view
#from rest_framework.response import Response

# imports for project
from api.models import TestAPI
from api.serializers import TestAPISerializer

# user auth imports
from django.contrib.auth.models import User
from api.serializers import UserSerializer



###########
# using generic class based (shortest)
###########

class APIList(generics.ListCreateAPIView):
    """
    List all API vals, or create a new API val.
    """
    queryset = TestAPI.objects.all()
    serializer_class = TestAPISerializer

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

class APIDetail(generics.RetrieveUpdateDestroyAPIView):
    """
    Retrieve, update, or delete an api instance.
    """
    queryset = TestAPI.objects.all()
    serializer_class = TestAPISerializer

# user auth views
class UserList(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class UserDetail(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


########### 
# using mixins
###########

#class APIList(mixins.ListModelMixin,
#              mixins.CreateModelMixin,
#              generics.GenericAPIView):
#    """
#    List all API vals, or create a new API val.
#    """
#    queryset = TestAPI.objects.all()
#    serializer_class = TestAPISerializer
#
#    def get(self, request, *args, **kwargs):
#        return self.list(request, *args, **kwargs)
#
#    def post(self, request, *args, **kwargs):
#        return self.create(request, *args, **kwargs)
#
#class APIDetail(mixins.RetrieveModelMixin,
#                mixins.UpdateModelMixin,
#                mixins.DestroyModelMixin,
#                generics.GenericAPIView):
#    """
#    Retrieve, update, or delete an api instance.
#    """
#    queryset = TestAPI.objects.all()
#    serializer_class = TestAPISerializer
#
#    def get(self, request, *args, **kwargs):
#        return self.retrieve(request, *args, **kwargs)
#
#    def put(self, request, *args, **kwargs):
#        return self.update(request, *args, **kwargs)
#
#    def delete(self, request, pk, format=None):
#        return self.destroy(request, *args, **kwargs)


########### 
# using rest APIView (class-based)
###########

#class APIList(APIView):
#    """
#    List all API vals, or create a new API val.
#    """
#    def get(self, request, format=None):
#        testapi = TestAPI.objects.all()
#        serializer = TestAPISerializer(testapi, many=True)
#        return Response(serializer.data)
#
#    def post(self, request, format=None):
#        serializer = TestAPISerializer(data=request.data)
#        if serializer.is_valid():
#            serializer.save()
#            return Response(serializer.data, status=status.HTTP_201_CREATED)
#        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#
#class APIDetail(APIView):
#    """
#    Retrieve, update, or delete an api instance.
#    """
#    def get_object(self, pk):
#        try:
#            return TestAPI.objects.get(pk=pk)
#        except TestAPI.DoesNotExist:
#            raise Http404
#
#    def get(self, request, pk, format=None):
#        testapi = self.get_object(pk)
#        serializer = TestAPISerializer(testapi)
#        return Response(serializer.data)
#
#    def put(self, request, pk, format=None):
#        testapi = self.get_object(pk)
#        serialzer = TestAPISerializer(testapi, data=request.data)
#        if serializer.is_valid():
#            serializer.save()
#            return Response(serializer.data)
#        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#
#    def delete(self, request, pk, format=None):
#        testapi = self.get_object(pk)
#        testapi.delete()
#        return Response(status=status.HTTP_204_NO_CONTENT)




######### 
# using rest api_view decorator (function-based)
#########

#@api_view(["GET", "POST"])
#def api_list(request, format=None):
#    """
#    List all testapi contents, or create a new testapi content.
#    """
#    if request.method == "GET":
#        testapi = TestAPI.objects.all()
#        serializer = TestAPISerializer(testapi, many=True)
#        return Response(serializer.data)
#
#    elif request.method == "POST":
#        serializer = TestAPISerializer(data=request.data)
#        if serializer.is_valid():
#            serializer.save()
#            return Response(serializer.data, status=status.HTTP_201_CREATED)
#        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#
#@api_view(["GET", "PUT", "DELETE"])
#def api_detail(request, pk, format=None):
#    """
#    Retrieve, update or delete an api instance.
#    """
#    try:
#        testapi = TestAPI.objects.get(pk=pk)
#    except TestAPI.DoesNotExist:
#        return Response(status=status.HTTP_404_NOT_FOUND)
#
#    if request.method == "GET":
#        serializer = TestAPISerializer(testapi)
#        return Response(serializer.data)
#
#    elif request.method == "PUT":
#        serializer = TestAPISerializer(testapi, data=request.data)
#        if serializer.is_valid():
#            serializer.save()
#            return Response(serializer.data)
#        return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)
#
#    elif request.method == "DELETE":
#        testapi.delete()
#        return Response(status=status.HTTP_204_NO_CONTENT)



######### 
# using default httpresponse method (not recommended)
#########

#class JSONResponse(HttpResponse):
#    """ JSON rendered HTTP response. """
#
#    def __init__(self, data, **kwargs):
#        content = JSONRenderer().render(data)
#        kwargs['content_type'] = 'application/json'
#        super(JSONResponse, self).__init__(content, **kwargs)
#
#@csrf_exempt
#def api_list(request):
#    """
#    List all code snippets, or create a new snippet.
#    """
#    if request.method == "GET":
#        testapi = TestAPI.objects.all()
#        serializer = TestAPISerializer(testapi, many=True)
#        return JSONResponse(serializer.data)
#    elif request.method == "POST":
#        data = JSONParser().parse(request)
#        serializer = TestAPISerializer(data=data)
#        if serializer.is_valid():
#            serializer.save()
#            return JSONResponse(serializer.data, status=201)
#        return JSONResponse(serializer.errors, status=400)
#def api_detail(request, pk):
#    """
#    Retrieve, update, or delete a code snippet.
#    """
#    try:
#        testapi = TestAPI.objects.get(pk=pk)
#    except TestAPI.DoesNotExist:
#        return HttpResponse(status=404)
#    if request.method == "GET":
#        serializer = TestAPISerializer(testapi)
#        return JSONResponse(serializer.data)
#    elif request.method == "PUT":
#        data = JSONParser().parse(request)
#        serializer = TestAPISerializer(testapi, data=data)
#        if serializer.is_valid():
#            serializer.save()
#            return JSONResponse(serializer.data)
#        return JSONResponse(serializer.errors, status=400)
#    elif request.method == "DELETE":
#        testapi.delete()
#        return HttpResponse(status=204)

