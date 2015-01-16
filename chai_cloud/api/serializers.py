from django.forms import widgets
from rest_framework import serializers
from api.models import Photo, Stores

class APISerializer(serializers.ModelSerializer):
    class Meta:
        model = Photo
        fields = ('path', 'title')

class StoresSerializer(serializers.ModelSerializer):
    class Meta:
        model = Stores
        fields = ('store_id', 'name', 'desc', 'phone', 'active')