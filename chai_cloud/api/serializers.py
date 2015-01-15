from django.forms import widgets
from rest_framework import serializers
from api.models import Photo

class APISerializer(serializers.ModelSerializer):
    class Meta:
        model = Photo
        fields = ('path', 'title')

