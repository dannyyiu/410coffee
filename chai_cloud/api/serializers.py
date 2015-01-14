from django.forms import widgets
from rest_framework import serializers
from api.models import TestAPI

from django.contrib.auth.models import User

## using serializer class
#class TestAPISerializer(serializers.Serializer):
#    pk = serializers.IntegerField(read_only=True)
#    title = serializers.CharField(
#            required=False, 
#            allow_blank=True, 
#            max_length=100)
#    code = serializers.CharField(style={'type': 'textarea'})
#
#    def create(self, validated_data):
#        """
#        Create and return a new TestAPI instance, given the validated data.
#        """
#        return TestAPI.objects.create(**validated_data)
#
#    def update(self, instance, validated_data):
#        """
#        Update and return an existing TestAPI instance, given the validated 
#        data.
#        """
#        instance.title = validated_data.get('title', instance.title)
#        instance.code = validated_data.get('code', instance.code)
#        instance.save()
#        return instance


## using model serializer class (shortcut of above)

class TestAPISerializer(serializers.ModelSerializer):
    class Meta:
        model = TestAPI
        owner = serializers.ReadOnlyField(source='owner.username')
        fields = ('id', 'title', 'code', 'owner')

class UserSerializer(serializers.ModelSerializer):
    testapi = serializers.PrimaryKeyRelatedField(many=True, 
                                             queryset=TestAPI.objects.all())
    class Meta:
        model = User
        fields = ('id', 'username', 'testapi',)