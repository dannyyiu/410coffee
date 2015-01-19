from django.forms import widgets
from rest_framework import serializers
from api.models import *

class APISerializer(serializers.ModelSerializer):
    class Meta:
        model = Photo
        fields = ('path', 'title')

class StoreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Store
        fields = ('store_id', 'name', 'desc', 'phone', 'active')
class InventorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Inventory
        fields = ('active', 'prod', 'store')